from abc import ABCMeta, abstractmethod

from generator.order.entities.order_pb2 import Order


# class for making orders
class OrderFactory:
	__metaclass__ = ABCMeta

	# initialization function
	# set order parameters_provider
	@abstractmethod
	def __init__(self, order_parameters_provider):
		self.order_parameters_provider = order_parameters_provider

	# make order with zone independent parameters
	# return Order
	@abstractmethod
	def make_order(self):
		order = Order()

		order.identifier = self.order_parameters_provider.generate_identifier()
		order.direction = self.order_parameters_provider.generate_direction()
		order.tag = self.order_parameters_provider.generate_tag()
		order.description = self.order_parameters_provider.generate_description()
		order.currency_pair = self.order_parameters_provider.generate_currency_pair()
		order.initial_px = self.order_parameters_provider.generate_initial_px()
		order.initial_volume = self.order_parameters_provider.generate_initial_volume()

		return order
