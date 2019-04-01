import sys
from pymysql.err import *

from service.database.service.db_service import DataBaseService
from config.config import Config


class MySQLService(DataBaseService):
	def __init__(self, logger, connection):
		super(__class__, self).__init__(logger, connection)

		self.uncommitted = 0

	def execute(self, query, number_of_queries_required_to_commit):
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(query)
			self.uncommitted += 1
			if self.uncommitted >= number_of_queries_required_to_commit:
				self.connection.commit()
				self.uncommitted = 0
		except Exception as ex:
			self.logger.error("Error occured while executing query to database: {}".format(sys.exc_info()[0]))
			self.logger.error(ex)
			self.logger.error("Query: " + query)
			self.connection.rollback()
