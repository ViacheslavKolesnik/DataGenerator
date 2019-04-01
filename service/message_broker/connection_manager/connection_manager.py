from abc import ABC, abstractmethod


class ConnectionManager(ABC):
	@abstractmethod
	def __init__(self, logger, user, password, host, virtual_host, port):
		self.logger = logger

		self.user = user
		self.password = password
		self.host = host
		self.virtual_host = virtual_host
		self.port = port

		self.connection = None

	@abstractmethod
	def open_connection(self):
		pass

	@abstractmethod
	def close_connection(self):
		pass

	@abstractmethod
	def _reconnect(self):
		pass
