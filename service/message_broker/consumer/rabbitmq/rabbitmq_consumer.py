from pika.exceptions import *
from threading import Thread

from config.constant.exit_code import EXIT_CODE_CONSUMING_ERROR
from config.constant.message_broker import RABBITMQ_CONSUMER_INACTIVITY_TIMEOUT
from service.message_broker.consumer.consumer import Consumer


class RabbitMQConsumer(Consumer, Thread):
	def __init__(self, logger, storage, message_broker, queue):
		Thread.__init__(self)
		super(RabbitMQConsumer, self).__init__(logger)
		self.__storage = storage
		self.message_broker = message_broker
		self.__queue = queue
		self.__is_stopped = False

	def start(self):
		Thread.start(self)

	def run(self):
		self.message_broker.open_connection()

		while not self.__is_stopped:
			channel = self.message_broker._get_channel()
			self._consume(channel)
			self.message_broker._close_channel(channel)

		self.message_broker.close_connection()

	def stop(self):
		self.__is_stopped = True

	def _consume(self, channel):
		try:
			for method, properties, body in channel.consume(queue=self.__queue, auto_ack=False, inactivity_timeout=RABBITMQ_CONSUMER_INACTIVITY_TIMEOUT):
				if not body:
					self.stop()
					break
				self._on_consume(body)
				channel.basic_ack(method.delivery_tag)
		except AMQPError as ex:
			self.logger.error("Consumer. AMQPError occurred while consuming from RabbitMQ.")
			self.logger.error(ex)
			self.logger.warn("Consumer. Reconnecting to message broker.")
			self.message_broker._reconnect()
			self.logger.info("Consumer. Successfully reconnected to message broker.")
		except Exception as ex:
			self.logger.fatal("Error occured while consuming from queue {0}".format(self.__queue))
			self.logger.fatal(ex)
			exit(EXIT_CODE_CONSUMING_ERROR)

	def _on_consume(self, message):
		self.__storage.put(message)

	def get_status_stopped(self):
		return self.__is_stopped
