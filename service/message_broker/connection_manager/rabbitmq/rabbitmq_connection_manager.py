import time
from pika.exceptions import *
from pika import PlainCredentials, BlockingConnection, ConnectionParameters

from config.constant.other import NUMBER_OF_RECONNECTS, RECONNECT_TIMEOUT
from config.constant.exit_code import *

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from service.message_broker.connection_manager.connection_manager import ConnectionManager


class RabbitMQConnectionManager(ConnectionManager):
	def __init__(self, logger, user, password, host, virtual_host, port):
		super(__class__, self).__init__(logger, user, password, host, virtual_host, port)
		self.connections = MemoryAllocationManager.get_list()

	def open_connection(self):
		connection = None
		try:
			connection = BlockingConnection(ConnectionParameters(
				credentials=PlainCredentials(username=self.user, password=self.password),
				host=self.host,
				port=self.port,
				virtual_host=self.virtual_host
			))
			self.connections.append(connection)
			self.logger.info("Connection established.")
		except AMQPConnectionError:
			self.logger.fatal("AMQPConnectionError occurred while connecting to RabbitMQ.")
			exit(EXIT_CODE_AMQP_CONNECTION_ERROR)
		except AMQPError:
			self.logger.fatal("AMQPError occurred while connecting to RabbitMQ.")
			exit(EXIT_CODE_AMQP_ERROR)

		return connection

	def close_connection(self, connection):
		try:
			connection.close()
			self.logger.info("Connection closed.")
		except ConnectionClosed as ex:
			self.logger.warn("Connection already closed.")
			self.logger.warn(ex)
		except AMQPError as ex:
			self.logger.warn("AMQPError occured while closing connection.")
			self.logger.warn(ex)
		except Exception as ex:
			self.logger.warn("Error occured while closing connection.")
			self.logger.warn(ex)

	def close_all_connections(self):
		for connection in self.connections:
			self.close_connection(connection)

	def _reconnect(self):
		for iterator in range(NUMBER_OF_RECONNECTS):
			connection = self.open_connection()
			if connection:
				return connection
			self.logger.warn("Reconnect failed.")
			if iterator < NUMBER_OF_RECONNECTS - 1:
				self.logger.warn("Waiting {0} seconds to retry.".format(RECONNECT_TIMEOUT))
				time.sleep(RECONNECT_TIMEOUT)

		self.logger.fatal("Reconnect retries exceeded.")
		exit(EXIT_CODE_RECONNECT_TIMEOUT)

	def __get_channel(self, connection):
		channel = connection.channel()
		return channel

	def get_channel(self, connection):
		channel = None
		try:
			channel = self.__get_channel(connection)
		except ConnectionClosed as e:
			self.logger.warn("Unable to get channel. Connection to RabbitMQ closed. Reconnecting.")
			connection = self._reconnect()
			self.logger.info("Successfully reconnected to RabbitMQ.")
			channel = self.__get_channel(connection)

		return channel

	def close_channel(self, channel):
		try:
			channel.close()
		except ChannelClosed:
			self.logger.warn('Got ChannelClosed while closing channel.')
