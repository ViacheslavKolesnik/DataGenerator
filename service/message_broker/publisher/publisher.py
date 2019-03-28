from abc import ABC, abstractmethod


class Publisher(ABC):
	@abstractmethod
	def __init__(self, connection_manager):
		self.connection_manager = connection_manager
		self.logger = connection_manager.logger

	@abstractmethod
	def publish(self, *args, serializer=None):
		pass

	@abstractmethod
	def publish_multiple(self, *args, serializer=None):
		pass
