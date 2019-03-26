from abc import ABCMeta, abstractmethod


# class for serializing data
class Serializer:
	__metaclass__ = ABCMeta

	# initialization function
	# set logger
	@abstractmethod
	def __init__(self, logger):
		self.logger = logger

	# serializes data
	# returns serialized data
	@abstractmethod
	def serialize(self, *args):
		pass
