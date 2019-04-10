from pymysql import connect, MySQLError
import time

from config.constant.exit_code import *
from config.constant.other import RECONNECT_TIMEOUT, NUMBER_OF_RECONNECTS

from service.database.connection_manager.connection_manager import ConnectionManager
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class MySQLConnectionManager(ConnectionManager):
	def __init__(self, logger, user, password, host, port, database_name):
		super(__class__, self).__init__(logger, user, password, host, port, database_name)
		self.connections = MemoryAllocationManager.get_list()

	def open_connection(self):
		self.logger.info("Trying to establish database connection.")
		connection = None
		try:
			connection = self._open_connection()
		except MySQLError:
			self.logger.warn("Error connecting to database. Reconnecting.")
			connection = self._reconnect()
			self.logger.info("Successfully reconnected to database.")

		return connection

	def _open_connection(self):
		connection = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database_name)
		self.connections.append(connection)
		self.logger.info("Database connection successfully established.")

		return connection

	def close_all_connections(self):
		for connection in self.connections:
			self.close_connection(connection)

	def close_connection(self, connection):
		try:
			connection.close()
			self.logger.info("Database connection successfully closed.")
		except MySQLError:
			self.logger.error("Error closing database connection.")

	def _reconnect(self):
		for iterator in range(NUMBER_OF_RECONNECTS):
			try:
				connection = self._open_connection()
				if connection:
					return connection
			except:
				self.logger.warn("Reconnect failed.")
				if iterator < NUMBER_OF_RECONNECTS - 1:
					self.logger.warn("Waiting {0} seconds to retry.".format(RECONNECT_TIMEOUT))
					time.sleep(RECONNECT_TIMEOUT)

		self.logger.fatal("Reconnect retries exceeded.")
		exit(EXIT_CODE_RECONNECT_TIMEOUT)
