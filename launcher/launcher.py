from __future__ import division

from math import ceil

from config.constants.constants_file import FILE_PERMISSION_DATA_OUTPUT

from logger.file_logger.file_logger import FileLogger
from config.config_parser import ConfigurationParser
from config.config import Config
from utils.utils import Utils
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from generator.order_generator.order_generator import OrderGenerator
from service.file_service.writer.writer_file_service import WriterFileService
from generator.order_generator.order_record_constructor.order_record_constructor import OrderRecordConstructor
from serializer.string_serializer.order_record_string_serializer.order_record_string_serializer import OrderRecordStringSerializer


# main program class
# handles program execution
class Launcher:
	# main initializing function of Data Generator
	# initialize logger
	# initialize utils
	# initialize memory allocation manager
	# parse configurations
	# initialize generator
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

		self.logger.info("Initializing writer file service.")
		self.writer_file_service = WriterFileService(self.logger, Config.file.data_output_file, FILE_PERMISSION_DATA_OUTPUT)


	# prepare to execute function
	def __prepare(self):
		pass

	# main execution function
	def __execute(self):
		self.logger.info("Starting data generator.")

		order_record_constructor = OrderRecordConstructor(self.logger)
		string_serializer = OrderRecordStringSerializer(self.logger)

		for iterator in range(int(ceil(Config.order.number_of_orders_total / Config.order.number_of_orders_per_chunk))):
			values = self.generator.generate(Config.order.number_of_orders_per_chunk)

			order_records = order_record_constructor.construct_records_from_orders(values)
			self.writer_file_service.write(order_records, string_serializer)

		self.logger.info("Generated {0} values.".format(self.generator.total_number_of_generated_values))



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
