from pika.exceptions import *

from service.message_broker.publisher.publisher import Publisher


class RabbitMQPublisher(Publisher):
	def __init__(self, connection_manager):
		super(__class__, self).__init__(connection_manager)

	def publish(self, exchange, routing_key, message, serializer=None):
		connection = self.connection_manager.open_connection()

		routing_key = message.status
		if serializer is not None:
			message = serializer.serialize(message)

		try:
			channel = connection.channel()
			channel.basic_publish(exchange=exchange,
								  routing_key=routing_key,
								  body=message)
			channel.close()
		except ChannelError:
			self.logger.fatal("ChannelError occured while publishing to RabbitMQ.")
		except AMQPError:
			self.logger.fatal("ChannelError occured while publishing to RabbitMQ.")
		except:
			self.logger.fatal("Error occured while publishing to RabbitMQ.")
		finally:
			self.connection_manager.close_connection(connection)

	def publish_multiple(self, exchange, messages, serializer=None):
		connection = self.connection_manager.open_connection()
		published_messages_counter = 0

		try:
			channel = connection.channel()

			for message in messages:
				routing_key = message.status
				if serializer is not None:
					message = serializer.serialize(message)
				channel.basic_publish(exchange=exchange,
									  routing_key=routing_key,
									  body=message)
				published_messages_counter += 1

			channel.close()
		except ChannelError:
			self.logger.fatal("ChannelError occured while publishing to RabbitMQ.")
		except AMQPError:
			self.logger.fatal("ChannelError occured while publishing to RabbitMQ.")
		except:
			self.logger.fatal("Error occured while publishing to RabbitMQ.")
		finally:
			self.connection_manager.close_connection(connection)
			self.logger.info("Published {0} messages.".format(published_messages_counter))
