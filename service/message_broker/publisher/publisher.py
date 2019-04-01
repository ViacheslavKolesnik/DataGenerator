from abc import ABC, abstractmethod


class Publisher(ABC):
	@abstractmethod
	def __init__(self, logger):
		self.logger = logger

	@abstractmethod
	def publish(self, *args):
		pass
