from abc import ABCMeta, abstractmethod

from serializer.serializer import Serializer


# class for serializing data into string
class StringSerializer(Serializer):
	__metaclass__ = ABCMeta

	# initialization function
	# set logger
	@abstractmethod
	def __init__(self, logger):
		super(StringSerializer, self).__init__(logger)

	# serializes data into string
	# returns string
	@abstractmethod
	def serialize(self, *args):
		pass
