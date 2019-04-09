from abc import ABCMeta, abstractmethod


# class for serializing data
class Serializer:
	__metaclass__ = ABCMeta

	# serializes data
	# returns serialized data
	@abstractmethod
	def serialize(self, *args):
		pass

	# deserializes data
	# returns deserialized data
	@abstractmethod
	def deserialize(self, *args):
		pass
