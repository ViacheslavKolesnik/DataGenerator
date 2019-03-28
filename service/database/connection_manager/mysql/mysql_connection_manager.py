from pymysql import connect, MySQLError

from config.constant.exit_code import *

from service.database.connection_manager.connection_manager import ConnectionManager
from config.config import Config


class MySQLConnectionManager(ConnectionManager):
	def __init__(self, logger, user, password, host, port, database_name):
		super(__class__, self).__init__(logger, user, password, host, port, database_name)

	def open_connection(self):
		self.logger.info("Trying to establish database connection.")
		database_connection = None

		try:
			database_connection = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database_name)
			self.logger.info("Database connection successfully established.")
		except MySQLError:
			self.logger.fatal("Error connecting to database.")
			exit(EXIT_CODE_DATABASE_CONNECTION_FAILED)

		return database_connection

	def close_connection(self, connection):
		try:
			connection.close()
			self.logger.info("Database connection successfully closed.")
		except MySQLError:
			self.logger.error("Error closing database connection.")
			exit(EXIT_CODE_DATABASE_CONNECTION_FAILED)
