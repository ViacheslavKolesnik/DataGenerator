from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from generator.order_generator.order_DTOs.order_record import OrderRecord


# class for constructing order records from orders
class OrderRecordConstructor:
	# initialization function
	# set logger
	def __init__(self, logger):
		self.logger = logger

	# construct list of records from list of orders
	# accept list of orders
	# return list of order records
	def construct_records_from_orders(self, orders):
		order_records = MemoryAllocationManager.get_list()

		for order in orders:
			one_order_records = self.__construct_records_from_order(order)
			order_records.extend(one_order_records)

		self.logger.info("Constructed {0} order records from {1} orders.".format(len(order_records), len(orders)))

		return order_records

	# construct list of records from order
	# accept order
	# return list of order records
	def __construct_records_from_order(self, order):
		records = MemoryAllocationManager.get_list()

		if order.status.start is not None:
			record = self.__construct_record_from_order(order)
			record.timestamp = order.timestamp.start
			record.status = order.status.start
			records.append(record)
		if order.status.intermediate is not None:
			record = self.__construct_record_from_order(order)
			record.timestamp = order.timestamp.intermediate
			record.status = order.status.intermediate
			records.append(record)
		if order.status.final is not None:
			record = self.__construct_record_from_order(order)
			record.timestamp = order.timestamp.final
			record.status = order.status.final
			record.fill_px = order.fill_px
			record.fill_volume = order.fill_volume
			records.append(record)

		return records

	# construct order record with parameters same for all records of one order
	# accept order
	# return order record
	def __construct_record_from_order(self, order):
		record = OrderRecord()

		record.identifier = order.identifier
		record.direction = order.direction
		record.currency_pair = order.currency_pair
		record.initial_px = order.initial_px
		record.initial_volume = order.initial_volume
		record.tag = order.tag
		record.description = order.description

		return record
