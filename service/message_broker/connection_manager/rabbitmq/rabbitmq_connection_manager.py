import time
from pika.exceptions import *
from pika import PlainCredentials, BlockingConnection, ConnectionParameters

from config.constant.other import NUMBER_OF_RECONNECTS, RECONNECT_TIMEOUT
from config.constant.exit_code import *

from service.message_broker.connection_manager.connection_manager import ConnectionManager


class RabbitMQConnectionManager(ConnectionManager):
	def __init__(self, logger, user, password, host, virtual_host, port):
		super(__class__, self).__init__(logger, user, password, host, virtual_host, port)

	def open_connection(self):
		try:
			if not self.connection or not self.connection.is_open:
				self.connection = BlockingConnection(ConnectionParameters(
					credentials=PlainCredentials(username=self.user, password=self.password),
					host=self.host,
					port=self.port,
					virtual_host=self.virtual_host
				))
				self.logger.info("Connection established.")
		except AMQPConnectionError:
			self.logger.fatal("AMQPConnectionError occurred while connecting to RabbitMQ.")
			exit(EXIT_CODE_AMQP_CONNECTION_ERROR)
		except AMQPError:
			self.logger.fatal("AMQPError occurred while connecting to RabbitMQ.")
			exit(EXIT_CODE_AMQP_ERROR)

	def close_connection(self):
		try:
			self.connection.close()
			self.logger.info("Connection closed.")
		except ConnectionClosed:
			self.logger.error("Connection already closed.")
		except AMQPError:
			self.logger.error("AMQPError occured while closing connection.")
		except:
			self.logger.error("Error occured while closing connection.")

	def _reconnect(self):
		for iterator in range(NUMBER_OF_RECONNECTS):
			self.open_connection()
			if self.connection:
				return
			self.logger.warn("Reconnect failed.")
			if iterator < NUMBER_OF_RECONNECTS - 1:
				self.logger.warn("Waiting {0} seconds to retry.".format(RECONNECT_TIMEOUT))
				time.sleep(RECONNECT_TIMEOUT)

		self.logger.fatal("Reconnect retries exceeded.")
		exit(EXIT_CODE_RECONNECT_TIMEOUT)

	def __get_channel(self):
		channel = self.connection.channel()
		return channel

	def get_channel(self):
		channel = None
		try:
			channel = self.__get_channel()
		except ConnectionClosed as e:
			self.logger.warn("Unable to get channel. Connection to RabbitMQ closed. Reconnecting.")
			self._reconnect()
			self.logger.info("Successfully reconnected to RabbitMQ.")
			channel = self.__get_channel()

		return channel

	def close_channel(self, channel):
		try:
			channel.close()
		except ChannelClosed:
			self.logger.warn('Got ChannelClosed while closing channel.')
