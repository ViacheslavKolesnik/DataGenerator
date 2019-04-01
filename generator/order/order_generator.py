from config.constant.linear_congruent import LIN_CON_STARTING_NUMBER

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from config.config import Config
from generator.generator import Generator
from generator.order.parameters_provider.order_parameters_provider import OrderParametersProvider
from generator.order.factory.implementation.red_zone_order_factory import RedZoneOrderFactory
from generator.order.factory.implementation.green_zone_order_factory import GreenZoneOrderFactory
from generator.order.factory.implementation.blue_zone_order_factory import BlueZoneOrderFactory
from metric.decorator.metric_decorator import timeit


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
	# accepts amount of orders to generate and metric instance
	# returns list of orders
	def generate(self, amount, metric):
		number_of_previously_generated_values = self.total_number_of_generated_values
		current_number_of_generated_values = 0
		order_records = MemoryAllocationManager.get_list()

		self.__generate_zone_dependent_order(order_records,
											 Config.order.number_of_orders_zone_red,
											 self.red_zone_order_factory,
											 amount,
											 current_number_of_generated_values,
											 metrics=metric.get_red_zone_order_generation())
		current_number_of_generated_values = self.total_number_of_generated_values - number_of_previously_generated_values

		green_zone_right_border_number = Config.order.number_of_orders_zone_red + Config.order.number_of_orders_zone_green
		self.__generate_zone_dependent_order(order_records,
											 green_zone_right_border_number,
											 self.green_zone_order_factory,
											 amount,
											 current_number_of_generated_values,
											 metrics=metric.get_green_zone_order_generation())
		current_number_of_generated_values = self.total_number_of_generated_values - number_of_previously_generated_values

		self.__generate_zone_dependent_order(order_records,
											 Config.order.number_of_orders_total,
											 self.blue_zone_order_factory,
											 amount,
											 current_number_of_generated_values,
											 metrics=metric.get_blue_zone_order_generation())

		return order_records

	# generates orders for specified zone
	# orders - list of orders
	# zone_right_border_number - max number of orders to be generated for specified zone
	# factory - factory that specifies zone for which orders are generated
	# amount - max amount of orders to be generated
	# current_number_of_generated_values - number of orders generated in current generation process
	@timeit
	def __generate_zone_dependent_order(self, order_records, zone_right_border_number, order_factory, amount, current_number_of_generated_values):
		if self.total_number_of_generated_values < zone_right_border_number:
			while self.total_number_of_generated_values < zone_right_border_number and current_number_of_generated_values < amount:
				generated_order_records = order_factory.make_order()
				order_records.extend(generated_order_records)
				current_number_of_generated_values += 1
				self.total_number_of_generated_values += 1
