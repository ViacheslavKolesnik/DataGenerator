import pika

from config.constant.message_broker import *
from service.message_broker.broker import MessageBroker


class RabbitMQ(MessageBroker):
	def __init__(self, logger, channel):
		super(RabbitMQ, self).__init__(logger)
		self.channel = channel

	def setup(self):
		super(RabbitMQ, self).setup()

		self.__exchange_declare(exchange=RABBITMQ_EXCHANGE,
								exchange_type=RABBITMQ_EXCHANGE_TYPE,
								passive=RABBITMQ_EXCHANGE_DECLARE_PASSIVE,
								durable=RABBITMQ_EXCHANGE_DURABLE)
		self.__queue_declare(queue=RABBITMQ_QUEUE_NEW,
								passive=RABBITMQ_QUEUE_DECLARE_PASSIVE,
								durable=RABBITMQ_QUEUE_DURABLE)
		self.__queue_declare(queue=RABBITMQ_QUEUE_TO_PROVIDER,
								passive=RABBITMQ_QUEUE_DECLARE_PASSIVE,
								durable=RABBITMQ_QUEUE_DURABLE)
		self.__queue_declare(queue=RABBITMQ_QUEUE_FINAL,
								passive=RABBITMQ_QUEUE_DECLARE_PASSIVE,
								durable=RABBITMQ_QUEUE_DURABLE)

		self.__queue_bind(queue=RABBITMQ_QUEUE_NEW,
						  exchange=RABBITMQ_EXCHANGE,
						  routing_key=RABBITMQ_QUEUE_BIND_ROUTING_KEY_NEW)
		self.__queue_bind(queue=RABBITMQ_QUEUE_TO_PROVIDER,
						  exchange=RABBITMQ_EXCHANGE,
						  routing_key=RABBITMQ_QUEUE_BIND_ROUTING_KEY_TO_PROVIDER)
		self.__queue_bind(queue=RABBITMQ_QUEUE_FINAL,
						  exchange=RABBITMQ_EXCHANGE,
						  routing_key=RABBITMQ_QUEUE_BIND_ROUTING_KEY_FILLED)
		self.__queue_bind(queue=RABBITMQ_QUEUE_FINAL,
						  exchange=RABBITMQ_EXCHANGE,
						  routing_key=RABBITMQ_QUEUE_BIND_ROUTING_KEY_PARTIAL_FILLED)
		self.__queue_bind(queue=RABBITMQ_QUEUE_FINAL,
						  exchange=RABBITMQ_EXCHANGE,
						  routing_key=RABBITMQ_QUEUE_BIND_ROUTING_KEY_REJECTED)

	def __exchange_declare(self, exchange=None, exchange_type='direct', passive=False, durable=False, auto_delete=False):
		try:
			self.channel.exchange_declare(exchange=exchange,
										  exchange_type=exchange_type,
										  passive=passive,
										  durable=durable,
										  auto_delete=auto_delete)
		except Exception as ex:
			self.logger.fatal("Error. Unable to declare exchange.")
			self.logger.fatal(ex)

	def __queue_declare(self, queue, passive=False, durable=False, exclusive=False, auto_delete=False):
		try:
			self.channel.queue_declare(queue=queue,
									   passive=passive,
									   durable=durable,
									   exclusive=exclusive,
									   auto_delete=auto_delete)
		except Exception as ex:
			self.logger.fatal("Error. Unable to declare queue.")
			self.logger.fatal(ex)

	def __queue_bind(self, queue, exchange, routing_key):
		try:
			self.channel.queue_bind(queue=queue,
									exchange=exchange,
									routing_key=routing_key)
		except Exception as ex:
			self.logger.fatal("Error. Unable to bind queue.")
			self.logger.fatal(ex)

