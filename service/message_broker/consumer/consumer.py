from abc import ABC, abstractmethod


class Consumer(ABC):
	@abstractmethod
	def __init__(self, logger, *args):
		self.logger = logger

	@abstractmethod
	def start(self):
		pass

	@abstractmethod
	def _consume(self, *args):
		pass

	@abstractmethod
	def _on_consume(self, *args):
		pass
