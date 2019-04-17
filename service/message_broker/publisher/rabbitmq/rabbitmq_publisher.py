import pika
from pika.exceptions import AMQPError
from time import perf_counter

from config.constant.exit_code import *
from config.constant.message_broker import RABBITMQ_MESSAGE_DELIVERY_MODE
from service.message_broker.publisher.publisher import Publisher


class RabbitMQPublisher(Publisher):
	def __init__(self, logger, message_broker, channel, exchange, routing_keys):
		super(__class__, self).__init__(logger)

		self.message_broker = message_broker
		self.channel = channel
		self.exchange = exchange
		self.routing_keys = routing_keys

	def publish(self, routing_key, message):
		try:
			self.channel.basic_publish(exchange=self.exchange,
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
			self.channel = self.message_broker._get_channel()
			self.logger.info("Publisher. Successfully reconnected to message broker.")
		except Exception as ex:
			self.logger.fatal("Error occured while publishing to RabbitMQ.")
			self.logger.fatal(ex)
			exit(EXIT_CODE_PUBLISH_ERROR)

		return False
