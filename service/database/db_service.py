from abc import ABC, abstractmethod


class DataBaseService(ABC):
	@abstractmethod
	def __init__(self, logger, user, password, host, port, database_name):
		self.logger = logger

		self.user = user
		self.password = password
		self.host = host
		self.port = port
		self.database_name = database_name

	@abstractmethod
	def open_connection(self, *args, **kwargs):
		pass

	@abstractmethod
	def close_connection(self, *args, **kwargs):
		pass

	@abstractmethod
	def _reconnect(self, *args, **kwargs):
		pass

	@abstractmethod
	def execute_one(self, *args, **kwargs):
		pass

	@abstractmethod
	def execute_many(self, *args, **kwargs):
		pass

	@abstractmethod
	def _execute(self, *args, **kwargs):
		pass

	@abstractmethod
	def execute_select(self, *args, **kwargs):
		pass
