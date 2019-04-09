from abc import ABCMeta, abstractmethod


# strategy class for modifying Order object
class OrderModifyStrategy:
	__metaclass__ = ABCMeta

	# modifying function
	@abstractmethod
	def modify(self, *args):
		pass
