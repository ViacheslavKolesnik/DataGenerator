from config.constants.constants_status import *
from config.constants.constants_datetime import NUMBER_OF_DATES_BLUE_ZONE

from order_factory import OrderFactory
from generator.order_generator.order_DTOs.order_status import OrderStatus
from generator.order_generator.order_DTOs.order_status_timestamp import OrderStatusTimeStamp


# class for making blue zone orders
class BlueZoneOrderFactory(OrderFactory):
	# initialization function
	# set order parameters_provider
	def __init__(self, order_parameters_provider):
		super(BlueZoneOrderFactory, self).__init__(order_parameters_provider)

	# make order with blue zone dependent parameters
	# return Order
	def make_order(self):
		order = super(BlueZoneOrderFactory, self).make_order()

		order_status = OrderStatus()
		order_status.start = STATUS_NEW
		order_status.intermediate = STATUS_TO_PROVIDER
		order.status = order_status

		order_status_timestamps = self.order_parameters_provider.generate_dates(NUMBER_OF_DATES_BLUE_ZONE)
		order_status_timestamp = OrderStatusTimeStamp()
		order_status_timestamp.start = order_status_timestamps[0]
		order_status_timestamp.intermediate = order_status_timestamps[1]
		order.timestamp = order_status_timestamp

		self.order_parameters_provider.update_provider()

		return order
