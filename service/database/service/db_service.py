from abc import ABC, abstractmethod


class DataBaseService(ABC):
	@abstractmethod
	def __init__(self, logger, connection_manager):
		self.logger = logger
		self.connection_manager = connection_manager

	@abstractmethod
	def execute(self, message, serializer=None):
		pass

	@abstractmethod
	def execute_multiple(self, messages, serializer=None):
		pass
