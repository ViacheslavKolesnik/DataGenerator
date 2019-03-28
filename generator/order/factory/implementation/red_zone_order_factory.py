from config.constant.status import *
from config.constant.datetime import NUMBER_OF_DATES_RED_ZONE

from generator.order.factory.order_factory import OrderFactory
from generator.order.entities.order_record_pb2 import OrderRecord
from generator.order.strategy.final_status_context import FinalStatusContext
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


# class for making red zone orders
class RedZoneOrderFactory(OrderFactory):
	# initialization function
	# set order parameters_provider
	def __init__(self, order_parameters_provider):
		super(RedZoneOrderFactory, self).__init__(order_parameters_provider)

	# make order with red zone dependent parameters
	# return Order
	def make_order(self):
		order = super(RedZoneOrderFactory, self).make_order()
		order_records = MemoryAllocationManager.get_list()

		order_record_to_provider = OrderRecord()
		order_record_to_provider.order.CopyFrom(order)
		order_record_final = OrderRecord()
		order_record_final.order.CopyFrom(order)

		order_record_to_provider.status = STATUS_TO_PROVIDER
		final_status = self.order_parameters_provider.generate_final_status()
		order_record_final.status = final_status

		fill_px = self.order_parameters_provider.generate_fill_px(order.initial_px)
		fill_volume = self.order_parameters_provider.generate_fill_volume(order.initial_volume)

		final_status_context = FinalStatusContext()
		final_status_strategy = final_status_context.get_strategy(final_status)
		final_status_strategy.modify(order_record_final.order, fill_px, fill_volume)

		order_status_timestamps = self.order_parameters_provider.generate_dates(NUMBER_OF_DATES_RED_ZONE)
		order_record_to_provider.timestamp = order_status_timestamps[0]
		order_record_final.timestamp = order_status_timestamps[1]

		order_records.append(order_record_to_provider)
		order_records.append(order_record_final)

		self.order_parameters_provider.update_provider()

		return order_records
