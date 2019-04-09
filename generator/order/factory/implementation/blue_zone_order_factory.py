from config.constant.status import *
from config.constant.datetime import NUMBER_OF_DATES_BLUE_ZONE

from generator.order.factory.order_factory import OrderFactory
from generator.order.entities.order_record import OrderRecord
from generator.order.strategy.final_status_context import FinalStatusContext
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


# class for making blue zone orders
class BlueZoneOrderFactory(OrderFactory):
	# initialization function
	# set order parameters_provider
	def __init__(self, order_parameters_provider):
		super(BlueZoneOrderFactory, self).__init__(order_parameters_provider)

	# make order with blue zone dependent parameters
	# return list of order records
	def make_order(self):
		order = super(BlueZoneOrderFactory, self).make_order()
		order_records = MemoryAllocationManager.get_list()

		order_record_new = OrderRecord()
		order_record_new.order = order
		order_record_to_provider = OrderRecord()
		order_record_to_provider.order = order

		order_record_new.status = STATUS_NEW
		order_record_to_provider.status = STATUS_TO_PROVIDER

		order_status_timestamps = self.order_parameters_provider.generate_dates(NUMBER_OF_DATES_BLUE_ZONE)
		order_record_new.timestamp = order_status_timestamps[0]
		order_record_to_provider.timestamp = order_status_timestamps[1]

		order_records.append(order_record_new)
		order_records.append(order_record_to_provider)

		self.order_parameters_provider.update_provider()

		return order_records
