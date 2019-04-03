from pika.exceptions import *

from config.constant.exit_code import *
from service.message_broker.publisher.publisher import Publisher


class RabbitMQPublisher(Publisher):
	def __init__(self, logger, channel):
		super(__class__, self).__init__(logger)

		self.channel = channel

	def publish(self, exchange, routing_key, message):
		try:
			self.channel.basic_publish(exchange=exchange,
								  routing_key=routing_key,
								  body=message)
		except ChannelError:
			self.logger.fatal("ChannelError occured while publishing to RabbitMQ.")
			exit(EXIT_CODE_CHANNEL_ERROR)
		except AMQPError:
			self.logger.fatal("AMQPError occured while publishing to RabbitMQ.")
			exit(EXIT_CODE_AMQP_ERROR)
		except:
			self.logger.fatal("Error occured while publishing to RabbitMQ.")
			exit(EXIT_CODE_PUBLISH_ERROR)
