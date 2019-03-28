import pika
from pika.exceptions import *
from pika import PlainCredentials, BlockingConnection, ConnectionParameters

from config.constant.exit_code import *

from service.message_broker.connection_manager.connection_manager import ConnectionManager
from config.config import Config


class RabbitMQConnectionManager(ConnectionManager):
	def __init__(self, logger, user, password, host, virtual_host, port):
		super(__class__, self).__init__(logger, user, password, host, virtual_host, port)

	def open_connection(self):
		connection = None
		try:
			connection = BlockingConnection(ConnectionParameters(
				credentials=PlainCredentials(username=self.user, password=self.password),
				host=self.host,
				port=self.port,
				virtual_host=self.virtual_host
			))
			self.logger.info("Connection established.")
		except AMQPConnectionError:
			self.logger.fatal("AMQPConnectionError occurred while connecting to RabbitMQ.")
			print("amqpconn err")
			exit(EXIT_CODE_AMQP_CONNECTION_ERROR)
		except AMQPError:
			print("amqp err")
			self.logger.fatal("AMQPError occurred while connecting to RabbitMQ.")
			exit(EXIT_CODE_AMQP_ERROR)

		return connection

	def close_connection(self, connection):
		try:
			connection.close()
			self.logger.info("Connection closed.")
		except ConnectionClosed:
			self.logger.error("Connection already closed.")
		except AMQPError:
			self.logger.error("AMQPError occured while closing connection.")
		except:
			self.logger.error("Error occured while closing connection.")
