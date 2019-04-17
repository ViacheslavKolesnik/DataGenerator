import sys
import mysql.connector
import time
from threading import current_thread

from config.constant.exit_code import *
from config.constant.other import RECONNECT_TIMEOUT, NUMBER_OF_RECONNECTS

from service.database.db_service import DataBaseService
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class MySQLService(DataBaseService):
	def __init__(self, logger, user, password, host, port, database_name):
		super(__class__, self).__init__(logger, user, password, host, port, database_name)

		self.connections = MemoryAllocationManager.get_dict()
		self.uncommitted = 0

	def open_connection(self):
		self.logger.info("Trying to establish database connection.")
		try:
			self._open_connection()
			self.logger.info("Database connection successfully established.")
		except mysql.connector.Error:
			self.logger.warn("Error connecting to database. Reconnecting.")
			self._reconnect()
			self.logger.info("Successfully reconnected to database.")

	# opens connection for current thread
	# append it to connections dictionary using current thread name as tag
	def _open_connection(self):
		connection_id = current_thread().name
		if connection_id in self.connections:
			if self.connections[connection_id].is_connected():
				self.logger.warn("Not opening database connection. It exists and already opened")
				return
		connection = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database_name)
		self.connections[connection_id] = connection

	def close_connection(self):
		try:
			connection = self._get_current_connection()
			connection.close()
			self.logger.info("Database connection successfully closed.")
		except Exception as ex:
			self.logger.error("Error closing database connection.")
			self.logger.error(ex)

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
			exit(EXIT_CODE_MYSQL_CONNECTION_DOES_NOT_EXIST)
		return connection

	def execute(self, query, number_of_queries_required_to_commit=1):
		connection = self._get_current_connection()
		try:
			cursor = connection.cursor()
			cursor.execute(query)
			cursor.close()
			self.uncommitted += 1
			if self.uncommitted >= number_of_queries_required_to_commit:
				connection.commit()
				self.uncommitted = 0
			return True
		except mysql.connector.ProgrammingError as ex:
			self.logger.error("ProgrammingError occured while executing query to database: {}".format(sys.exc_info()[0]))
			self.logger.error(ex)
			self.logger.error("Query: " + query)
			try:
				connection.rollback()
			except:
				pass
			return False
		except mysql.connector.Error as ex:
			self.logger.error("Error occurred while executing query to database.")
			self.logger.error(ex)
			self.logger.warn("Reconnecting to database.")
			self._reconnect()
			self.logger.info("Successfully reconnected to database.")
			return False

	def execute_select(self, query):
		connection = self._get_current_connection()
		response = None
		try:
			cursor = connection.cursor(dictionary=True)
			cursor.execute(query)
			response = cursor.fetchall()
			cursor.close()
		except mysql.connector.ProgrammingError as ex:
			self.logger.error("ProgrammingError occured while executing query to database: {}".format(sys.exc_info()[0]))
			self.logger.error(ex)
			self.logger.error("Query: " + query)
		except mysql.connector.Error as ex:
			self.logger.error("Error occurred while executing query to database.")
			self.logger.error(ex)
			self.logger.warn("Reconnecting to database.")
			self._reconnect()
			self.logger.info("Successfully reconnected to database.")

		return response
