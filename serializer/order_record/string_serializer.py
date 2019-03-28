from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from serializer.serializer import Serializer


# class for serializing order records into strings
class OrderRecordStringSerializer(Serializer):

	# initialization function
	# set logger
	def __init__(self, logger):
		super(OrderRecordStringSerializer, self).__init__(logger)

	# serialize order records into strings
	# accepts list of order records
	# returns list of strings
	def serialize(self, order_record):
		serialized_order_record = str(order_record.SerializeToString())

		return serialized_order_record
