from abc import ABC, abstractmethod


class ConnectionManager(ABC):
	@abstractmethod
	def __init__(self, logger, user, password, host, port, database_name):
		self.logger = logger

		self.user = user
		self.password = password
		self.host = host
		self.port = port
		self.database_name = database_name

	@abstractmethod
	def open_connection(self):
		pass
	@abstractmethod
	def close_connection(self, connection):
		pass
