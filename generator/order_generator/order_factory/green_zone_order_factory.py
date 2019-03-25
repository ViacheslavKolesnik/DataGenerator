from config.constants.constants_status import *
from config.constants.constants_datetime import NUMBER_OF_DATES_GREEN_ZONE

from order_factory import OrderFactory
from generator.order_generator.order_DTOs.order_status import OrderStatus
from generator.order_generator.order_DTOs.order_status_timestamp import OrderStatusTimeStamp

class GreenZoneOrderFactory(OrderFactory):
	def __init__(self, order_parameters_provider):
		super(GreenZoneOrderFactory, self).__init__(order_parameters_provider)

	def make_order(self):
		order = super(GreenZoneOrderFactory, self).make_order()

		order_status = OrderStatus()
		order_status.start = STATUS_NEW
		order_status.intermediate = STATUS_TO_PROVIDER
		order_status.final = self.order_parameters_provider.generate_final_status()
		order.status = order_status

		if order.status.final == STATUS_FILLED:
			order.fill_px = self.order_parameters_provider.generate_fill_px(order.initial_px)
			order.fill_volume = order.initial_volume
		elif order.status.final == STATUS_PARTIAL_FILLED:
			order.fill_px = self.order_parameters_provider.generate_fill_px(order.initial_px)
			order.fill_volume = self.order_parameters_provider.generate_fill_volume(order.initial_volume)

		order_status_timestamps = self.order_parameters_provider.generate_dates(NUMBER_OF_DATES_GREEN_ZONE)
		order_status_timestamp = OrderStatusTimeStamp()
		order_status_timestamp.start = order_status_timestamps[0]
		order_status_timestamp.intermediate = order_status_timestamps[1]
		order_status_timestamp.final = order_status_timestamps[2]
		order.timestamp = order_status_timestamp

		self.order_parameters_provider.update_provider()

		return order
