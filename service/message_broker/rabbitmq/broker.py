import pika

from config.constant.message_broker import *
from service.message_broker.broker import MessageBroker
from service.message_broker.publisher.rabbitmq.rabbitmq_publisher import RabbitMQPublisher
from service.message_broker.consumer.rabbitmq.rabbitmq_consumer import RabbitMQConsumer
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class RabbitMQ(MessageBroker):
	def __init__(self, logger, connection):
		super(RabbitMQ, self).__init__(logger)
		self.connection = connection
		self.publishers = MemoryAllocationManager.get_list()
		self.consumers = MemoryAllocationManager.get_list()

	def add_publisher(self, exchange, exchange_type, queue, routing_keys):
		channel = self.connection.channel()
		self.__setup_publisher(channel, exchange, exchange_type, queue, routing_keys)

		publisher = RabbitMQPublisher(self.logger, channel, exchange, routing_keys)

		self.publishers.append(publisher)

	def add_consumer(self, message_broker_connection_manager, storage, queue):
		channel = self.connection.channel()
		self.__setup_consumer(channel, queue)

		consumer = RabbitMQConsumer(self.logger, storage, message_broker_connection_manager, queue)

		self.consumers.append(consumer)

	def start_consumers(self):
		for consumer in self.consumers:
			consumer.start()

	def __setup_publisher(self, channel, exchange, exchange_type, queue, routing_keys):
		self.__exchange_declare(channel,
								exchange=exchange,
								exchange_type=exchange_type,
								passive=RABBITMQ_EXCHANGE_DECLARE_PASSIVE,
								durable=RABBITMQ_EXCHANGE_DURABLE)
		self.__queue_declare(channel,
							 queue=queue,
							 passive=RABBITMQ_QUEUE_DECLARE_PASSIVE,
							 durable=RABBITMQ_QUEUE_DURABLE)
		for routing_key in routing_keys:
			self.__queue_bind(channel,
							  queue=queue,
							  exchange=exchange,
							  routing_key=routing_key)

	def __setup_consumer(self, channel, queue):
		self.__queue_declare(channel,
							 queue=queue,
							 passive=RABBITMQ_QUEUE_DECLARE_PASSIVE,
							 durable=RABBITMQ_QUEUE_DURABLE)

	def __exchange_declare(self, channel, exchange=None, exchange_type='direct', passive=False, durable=False, auto_delete=False):
		try:
			channel.exchange_declare(exchange=exchange,
										  exchange_type=exchange_type,
										  passive=passive,
										  durable=durable,
										  auto_delete=auto_delete)
		except Exception as ex:
			self.logger.fatal("Error. Unable to declare exchange.")
			self.logger.fatal(ex)

	def __queue_declare(self, channel, queue, passive=False, durable=False, exclusive=False, auto_delete=False):
		try:
			channel.queue_declare(queue=queue,
									   passive=passive,
									   durable=durable,
									   exclusive=exclusive,
									   auto_delete=auto_delete)
		except Exception as ex:
			self.logger.fatal("Error. Unable to declare queue.")
			self.logger.fatal(ex)

	def __queue_bind(self, channel, queue, exchange, routing_key):
		try:
			channel.queue_bind(queue=queue,
									exchange=exchange,
									routing_key=routing_key)
		except Exception as ex:
			self.logger.fatal("Error. Unable to bind queue.")
			self.logger.fatal(ex)

