from abc import ABC, abstractmethod


class MessageBroker(ABC):
	@abstractmethod
	def __init__(self, logger, *args):
		self.logger = logger

	@abstractmethod
	def setup(self, *args):
		pass
