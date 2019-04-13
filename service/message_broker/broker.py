from abc import ABC, abstractmethod


class MessageBroker(ABC):
	@abstractmethod
	def __init__(self, logger, user, password, host, virtual_host, port):
		self.logger = logger

		self.user = user
		self.password = password
		self.host = host
		self.virtual_host = virtual_host
		self.port = port

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
	def add_publisher(self, *args, **kwargs):
		pass

	@abstractmethod
	def add_consumer(self, *args, **kwargs):
		pass
