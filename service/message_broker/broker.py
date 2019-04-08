from abc import ABC, abstractmethod


class MessageBroker(ABC):
	@abstractmethod
	def __init__(self, logger, *args):
		self.logger = logger

	@abstractmethod
	def add_publisher(self, *args):
		pass

	@abstractmethod
	def add_consumer(self, *args):
		pass
