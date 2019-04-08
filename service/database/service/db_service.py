from abc import ABC, abstractmethod


class DataBaseService(ABC):
	@abstractmethod
	def __init__(self, logger, connection):
		self.logger = logger
		self.connection = connection

	@abstractmethod
	def execute(self, *args):
		pass

	@abstractmethod
	def execute_select(self, *args):
		pass
