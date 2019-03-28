import sys
from pymysql.err import *

from service.database.service.db_service import DataBaseService


class MySQLService(DataBaseService):
	def __init__(self, logger, connection_manager):
		super(__class__, self).__init__(logger, connection_manager)

	def execute(self, message, serializer=None):
		query = message
		if serializer is not None:
			query = serializer.serialize(message)

		connection = self.connection_manager.open_connection()

		try:
			with connection.cursor() as cursor:
				cursor.execute(query)
				connection.commit()
		except:
			self.logger.error("Error occured while executing query to database: " + str(sys.exc_info()[0]))
			self.logger.error("Invalid query: " + query)
		finally:
			self.connection_manager.close_connection(connection)

	def execute_multiple(self, messages, serializer=None):
		number_of_executed_queries = 0

		connection = self.connection_manager.open_connection()

		try:
			with connection.cursor() as cursor:
				for message in messages:
					query = message
					if serializer is not None:
						query = serializer.serialize(message)
					cursor.execute(query)
					number_of_executed_queries += 1
				connection.commit()
		except MySQLError as e:
			self.logger.error("MySQLError occured while executing queries to database: " + str(sys.exc_info()[0]))
			self.logger.error(e)
		except DatabaseError as e:
			self.logger.error("DatabaseError occured while executing queries to database: " + str(sys.exc_info()[0]))
			self.logger.error(e)
		except:
			self.logger.error("Error occured while executing queries to database: " + str(sys.exc_info()[0]))
		finally:
			self.connection_manager.close_connection(connection)
			self.logger.info("Executed {0} queries to database.".format(number_of_executed_queries))
