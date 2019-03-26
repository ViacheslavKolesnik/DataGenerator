from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from serializer.string_serializer.string_serializer import StringSerializer


# class for serializing order records into strings
class OrderRecordStringSerializer(StringSerializer):

	# initialization function
	# set logger
	def __init__(self, logger):
		super(OrderRecordStringSerializer, self).__init__(logger)

	# serialize order records into strings
	# accepts list of order records
	# returns list of strings
	def serialize(self, order_records):
		serialized_order_records = MemoryAllocationManager.get_list()

		for order_record in order_records:
			serialized_order_record = self.__get_string_from_order_record(order_record)
			serialized_order_records.append(serialized_order_record)

		self.logger.info("Serialized {0} order records.".format(len(serialized_order_records)))

		return serialized_order_records

	# serialize order record into string
	# accepts order record
	# returns string
	def __get_string_from_order_record(self, order_record):
		string_order_record = ""

		string_order_record += order_record.identifier + " | "
		string_order_record += str(order_record.timestamp) + " | "
		string_order_record += order_record.status + " | "
		string_order_record += order_record.direction + " | "
		string_order_record += order_record.currency_pair + " | "
		string_order_record += str(order_record.initial_px) + " | "
		string_order_record += str(order_record.fill_px) + " | "
		string_order_record += str(order_record.initial_volume) + " | "
		string_order_record += str(order_record.fill_volume) + " | "
		string_order_record += order_record.tag + " | "
		string_order_record += order_record.description

		return string_order_record
