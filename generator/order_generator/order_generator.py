from config.constants.constants_linear_congruent import LIN_CON_STARTING_NUMBER

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from config.config import Config
from generator.generator import Generator
from order_parameters_provider.order_parameters_provider import OrderParametersProvider
from order_factory.red_zone_order_factory import RedZoneOrderFactory
from order_factory.green_zone_order_factory import GreenZoneOrderFactory
from order_factory.blue_zone_order_factory import BlueZoneOrderFactory


# class for generating orders
class OrderGenerator(Generator):
	# initialization function
	# creating order parameters provider
	# creating order factories and passing them order parameters provider
	# red_zone_order_factory - factory for making red zone orders
	# green_zone_order_factory - factory for making green zone orders
	# blue_zone_order_factory - factory for making blue zone orders
	def __init__(self, logger):
		super(OrderGenerator, self).__init__(logger)
		order_parameters_provider = OrderParametersProvider(LIN_CON_STARTING_NUMBER, Config.date.starting_date)
		self.red_zone_order_factory = RedZoneOrderFactory(order_parameters_provider)
		self.green_zone_order_factory = GreenZoneOrderFactory(order_parameters_provider)
		self.blue_zone_order_factory = BlueZoneOrderFactory(order_parameters_provider)

	# generation function
	# accepts amount of orders to generate
	# returns list of orders
	def generate(self, amount):
		number_of_previously_generated_values = self.total_number_of_generated_values
		current_number_of_generated_values = 0
		orders = MemoryAllocationManager.get_list()

		self.__generate_zone_dependent_order(orders, Config.order.number_of_orders_zone_red, self.red_zone_order_factory, amount, current_number_of_generated_values)
		current_number_of_generated_values = self.total_number_of_generated_values - number_of_previously_generated_values

		green_zone_right_border_number = Config.order.number_of_orders_zone_red + Config.order.number_of_orders_zone_green
		self.__generate_zone_dependent_order(orders, green_zone_right_border_number, self.green_zone_order_factory, amount, current_number_of_generated_values)
		current_number_of_generated_values = self.total_number_of_generated_values - number_of_previously_generated_values

		self.__generate_zone_dependent_order(orders, Config.order.number_of_orders_total, self.blue_zone_order_factory, amount, current_number_of_generated_values)

		return orders

	# generates orders for specified zone
	# orders - list of orders
	# zone_right_border_number - max number of orders to be generated for specified zone
	# order_factory - factory that specifies zone for which orders are generated
	# amount - max amount of orders to be generated
	# current_number_of_generated_values - number of orders generated in current generation process
	def __generate_zone_dependent_order(self, orders, zone_right_border_number, order_factory, amount, current_number_of_generated_values):
		if self.total_number_of_generated_values < zone_right_border_number:
			while self.total_number_of_generated_values < zone_right_border_number and current_number_of_generated_values < amount:
				order = order_factory.make_order()
				orders.append(order)
				current_number_of_generated_values += 1
				self.total_number_of_generated_values += 1
