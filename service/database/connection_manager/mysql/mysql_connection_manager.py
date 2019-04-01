from pymysql import connect, MySQLError
import time

from config.constant.exit_code import *
from config.constant.other import RECONNECT_TIMEOUT, NUMBER_OF_RECONNECTS

from service.database.connection_manager.connection_manager import ConnectionManager
from config.config import Config


class MySQLConnectionManager(ConnectionManager):
	def __init__(self, logger, user, password, host, port, database_name):
		super(__class__, self).__init__(logger, user, password, host, port, database_name)

	def open_connection(self):
		self.logger.info("Trying to establish database connection.")

		try:
			self._open_connection()
		except MySQLError:
			self.logger.warn("Error connecting to database. Reconnecting.")
			self._reconnect()
			self.logger.info("Successfully reconnected to database.")

	def _open_connection(self):
		self.connection = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database_name)
		self.logger.info("Database connection successfully established.")

	def close_connection(self):
		try:
			self.connection.close()
			self.logger.info("Database connection successfully closed.")
		except MySQLError:
			self.logger.error("Error closing database connection.")
			exit(EXIT_CODE_DATABASE_CONNECTION_FAILED)

	def _reconnect(self):
		for iterator in range(NUMBER_OF_RECONNECTS):
			try:
				self._open_connection()
				return
			except:
				self.logger.warn("Reconnect failed.")
				if iterator < NUMBER_OF_RECONNECTS - 1:
					self.logger.warn("Waiting {0} seconds to retry.".format(RECONNECT_TIMEOUT))
					time.sleep(RECONNECT_TIMEOUT)

		self.logger.fatal("Reconnect retries exceeded.")
		exit(EXIT_CODE_RECONNECT_TIMEOUT)
