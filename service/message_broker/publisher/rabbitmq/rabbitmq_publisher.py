from threading import Thread

import pika
from pika.exceptions import AMQPError

from config.constant.exit_code import *
from config.constant.message_broker import RABBITMQ_MESSAGE_DELIVERY_MODE
from service.message_broker.publisher.publisher import Publisher
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class RabbitMQPublisher(Publisher, Thread):
	def __init__(self, logger, message_broker, exchange, routing_keys):
		Thread.__init__(self)
		super(__class__, self).__init__(logger)

		self.message_broker = message_broker
		self.exchange = exchange
		self.routing_keys = routing_keys
		self.__queue = MemoryAllocationManager.get_dict()
		self.__is_stopped = False

	def run(self):
		self.message_broker.open_connection()

		while not self.__is_stopped or not len(self.__queue) == 0:
			channel = self.message_broker._get_channel()
			channel.confirm_delivery()
			keys = list(self.__queue.keys())
			for message in keys:
				publish_success = self.publish(channel, self.__queue[message], message)
				if publish_success:
					del self.__queue[message]
				else:
					break
			self.message_broker._close_channel(channel)

		self.message_broker.close_connection()

	def stop(self):
		self.__is_stopped = True

	def publish(self, channel, routing_key, message):
		try:
			channel.basic_publish(exchange=self.exchange,
									   routing_key=routing_key,
									   body=message,
									   properties=pika.BasicProperties(
										   delivery_mode = RABBITMQ_MESSAGE_DELIVERY_MODE,
									   ))
			return True
		except AMQPError as ex:
			self.logger.error("Publisher. AMQPError occured while publishing to RabbitMQ.")
			self.logger.error(ex)
			self.logger.warn("Publisher. Reconnecting to message broker.")
			self.message_broker._reconnect()
			self.logger.info("Publisher. Successfully reconnected to message broker.")
		except Exception as ex:
			self.logger.fatal("Error occured while publishing to RabbitMQ.")
			self.logger.fatal(ex)
			exit(EXIT_CODE_PUBLISH_ERROR)

		return False

	def enqueue(self, routing_key, message):
		self.__queue[message] = routing_key
