import time
import pika
from pika.exceptions import *
from threading import current_thread

from config.constant.exit_code import *
from config.constant.message_broker import *
from config.constant.other import *
from service.message_broker.broker import MessageBroker
from service.message_broker.publisher.rabbitmq.rabbitmq_publisher import RabbitMQPublisher
from service.message_broker.consumer.rabbitmq.rabbitmq_consumer import RabbitMQConsumer
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class RabbitMQ(MessageBroker):
	def __init__(self, logger, user, password, host, virtual_host, port):
		super(RabbitMQ, self).__init__(logger, user, password, host, virtual_host, port)

		self.connections = MemoryAllocationManager.get_dict()
		self.publishers = MemoryAllocationManager.get_list()
		self.consumers = MemoryAllocationManager.get_list()

	def open_connection(self):
		self.logger.info("Trying to establish message broker connection.")
		try:
			self._open_connection()
			self.logger.info("Message broker connection successfully established.")
		except AMQPError:
			self.logger.warn("Error connecting to message broker. Reconnecting.")
			self._reconnect()
			self.logger.info("Successfully reconnected to message broker.")

	# opens connection for current thread
	# append it to connections dictionary using current thread name as tag
	def _open_connection(self):
		connection_id = current_thread().name
		if connection_id in self.connections:
			if self.connections[connection_id].is_open:
				self.logger.warn("Not opening message broker connection. It exists and already opened")
				return
		connection = pika.BlockingConnection(pika.ConnectionParameters(
				credentials=pika.PlainCredentials(username=self.user, password=self.password),
				host=self.host,
				port=self.port,
				virtual_host=self.virtual_host
		))
		self.connections[connection_id] = connection

	def close_connection(self):
		try:
			connection = self._get_current_connection()
			connection.close()
			self.logger.info("Message broker connection successfully closed.")
		except Exception as ex:
			self.logger.warn("Error occured while closing connection.")
			self.logger.warn(ex)

	def _reconnect(self):
		for iterator in range(NUMBER_OF_RECONNECTS):
			try:
				self._open_connection()
				return
			except Exception as ex:
				self.logger.warn("Reconnect failed.")
				self.logger.warn(ex)
				if iterator < NUMBER_OF_RECONNECTS - 1:
					self.logger.warn("Waiting {0} seconds to retry.".format(RECONNECT_TIMEOUT))
					time.sleep(RECONNECT_TIMEOUT)

		self.logger.fatal("Reconnect retries exceeded.")
		exit(EXIT_CODE_RECONNECT_TIMEOUT)

	def _get_current_connection(self):
		connection_id = current_thread().name
		connection = None
		try:
			connection = self.connections[connection_id]
		except KeyError:
			self.logger.fatal("Connection for thread {} doesn't exist.".format(connection_id))
			exit(EXIT_CODE_MESSAGE_BROKER_CONNECTION_DOES_NOT_EXIST)
		return connection

	def __get_channel(self):
		connection = self._get_current_connection()
		channel = connection.channel()
		return channel

	def _get_channel(self):
		channel = None
		try:
			channel = self.__get_channel()
		except ConnectionError as ex:
			self.logger.warn("Unable to get channel. ConnectionError. Reconnecting to message broker.")
			self._reconnect()
			self.logger.info("Successfully reconnected to message broker.")
			try:
				channel = self.__get_channel()
			except AMQPError:
				self.logger.fatal("AMQPError occurred while reopening message broker channel.")
				exit(EXIT_CODE_AMQP_ERROR)
		except AMQPError:
			self.logger.fatal("AMQPError occurred while opening message broker channel.")
			exit(EXIT_CODE_AMQP_ERROR)

		return channel

	def _close_channel(self, channel):
		try:
			channel.close()
		except Exception as ex:
			self.logger.error('Error closing channel.')
			self.logger.error(ex)

	def add_publisher(self, exchange, exchange_type, queue, routing_keys):
		channel = self._get_channel()
		self.__setup_publisher(channel, exchange, exchange_type, queue, routing_keys)

		publisher = RabbitMQPublisher(self.logger, channel, exchange, routing_keys)

		self.publishers.append(publisher)

	def add_consumer(self, storage, queue):
		channel = self._get_channel()
		self.__setup_consumer(channel, queue)

		consumer = RabbitMQConsumer(self.logger, storage, self, queue)

		self.consumers.append(consumer)

	def start_consumers(self):
		for consumer in self.consumers:
			consumer.start()

	def stop_consumers(self):
		for consumer in self.consumers:
			consumer.stop()

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

