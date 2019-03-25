from logger.file_logger.file_logger import FileLogger
from config.config_parser import ConfigurationParser
from config.config import Config
from utils.utils import Utils
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from generator.order_generator.order_generator import OrderGenerator


# main program class
# handles program execution
class Launcher:
	# main initializing function of Data Generator
	# initialize logger
	def __init__(self):
		self.logger = FileLogger()
		self.logger.info("Logger initialized. Initializing data generator.")
		self.logger.info("Initializing utils.")
		Utils.initialize(self.logger)
		self.logger.info("Initializing memory allocation manager.")
		MemoryAllocationManager.initialize(self.logger)
		self.logger.info("Parsing config files.")
		ConfigurationParser(self.logger).parse_config()
		
		self.logger.info("Initializing generator.")
		self.generator = OrderGenerator(self.logger)


	# prepare to execute function
	def __prepare(self):
		pass

	# main execution function
	def __execute(self):
		self.logger.info("Starting data generator.")
		for iterator in range(int(Config.order.number_of_orders_total / Config.order.number_of_orders_per_chunk)):
			values = self.generator.generate(Config.order.number_of_orders_per_chunk)
			self.logger.info("Generated {0} orders.".format(len(values)))

	# reporting function
	def __report(self):
		pass

	# main finish function
	def __finish(self):
		pass

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		self.__execute()
		self.__report()
		self.__finish()


# Entry point to Data Generator
if __name__ == "__main__":
	launcher = Launcher()
	launcher.launch()
