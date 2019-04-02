from math import ceil
from datetime import datetime

from config.constant.file import *
from config.constant.message_broker import RABBITMQ_EXCHANGE
from config.constant.other import SECOND_TO_MICROSECOND_CONVERTING_COEF
from config.constant.config import DEFAULT_CONFIG_FILES

from logger.file_logger.file_logger import FileLogger
from config.parser.ini.ini_config_parser import INIConfigurationParser
from config.config import Config
from utils.utils import Utils
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from generator.order.order_generator import OrderGenerator
from service.file_service.writer.writer_file_service import FileWriter
from service.file_service.reader.reader_file_service import ReaderFileService
from serializer.order_record.serializer import OrderRecordSerializer
from service.message_broker.connection_manager.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager
from service.message_broker.publisher.rabbitmq.rabbitmq_publisher import RabbitMQPublisher
from service.database.query_constructor.order_record.query_constructor import OrderRecordDBQueryConstructor
from service.database.connection_manager.mysql.mysql_connection_manager import MySQLConnectionManager
from service.database.service.mysql.mysql_service import MySQLService
from reporter.reporter import Reporter
from generator.order.parser.order_record_from_string import OrderRecordFromString
from metric.generator.order_generator.metric import OrderGeneratorMetric
from metric.decorator.metric_decorator import timeit


# main program class
# handles program execution
class Launcher:
	# main initializing function of Data Generator
	# initialize logger
	# initialize utils
	# initialize memory allocation manager
	# parse configurations
	# initialize order_generator
	def __initialize(self, program_start_time):
		logger = FileLogger(program_start_time)
		logger.info("Logger initialized. Initializing data order_generator.")

		logger.info("Initializing utils.")
		Utils.initialize(logger)

		logger.info("Initializing memory allocation manager.")
		MemoryAllocationManager.initialize(logger)

		logger.info("Parsing config files.")
		INIConfigurationParser(logger, DEFAULT_CONFIG_FILES).parse_config()

		logger.info("Setting log level.")
		logger.set_log_level(Config.log.log_level)

		message_broker_connection_manager = RabbitMQConnectionManager(logger,
													   user=Config.message_broker.user,
													   password=Config.message_broker.password,
													   host=Config.message_broker.host,
													   virtual_host=Config.message_broker.virtual_host,
													   port=Config.message_broker.port)
		message_broker_connection_manager.open_connection()

		db_connection_manager = MySQLConnectionManager(logger,
													   user=Config.database.user,
													   password=Config.database.password,
													   host=Config.database.host,
													   port=Config.database.port,
													   database_name=Config.database.database_name)
		db_connection_manager.open_connection()

		return logger, message_broker_connection_manager, db_connection_manager

	# main execution function
	def __execute(self, logger, message_broker_connection_manager, db_connection_manager, program_start_time):
		logger.info("Starting data order_generator.")
		generator = OrderGenerator(logger)

		data_output_file = Config.file.data_output_file_path + program_start_time + FILE_EXTENSION_DATA_OUTPUT
		writer_file_service = FileWriter(logger, data_output_file, FILE_PERMISSION_DATA_OUTPUT)
		reader_file_service = ReaderFileService(logger, data_output_file, FILE_PERMISSION_READ_DATA_OUTPUT)

		serializer = OrderRecordSerializer()

		channel = message_broker_connection_manager.get_channel()
		publisher = RabbitMQPublisher(logger, channel)

		db_query_constructor = OrderRecordDBQueryConstructor()
		db_service = MySQLService(logger, db_connection_manager.connection)

		metric = OrderGeneratorMetric()

		file_read_seek_number = 0

		for iterator in range(int(ceil(Config.order.number_of_orders_total / Config.order.number_of_orders_per_chunk))):
			values = self.__generate(generator, metric, metrics=metric.get_generation())

			self.__write(writer_file_service, values, metrics=metric.get_file_insertion())

			self.__publish(serializer, publisher, values, metrics=metric.get_message_broker_publishing())

			values_from_file = self.__read_and_parse_from_file(reader_file_service, file_read_seek_number, metrics=metric.get_file_reading_and_parsing())
			file_read_seek_number += len(values_from_file)

			self.__write_to_db(values, db_query_constructor, db_service, metrics=metric.get_database_writing())

		logger.info("Generated {0} values.".format(generator.total_number_of_generated_values))

		return metric

	@timeit
	def __generate(self, generator, metric):
		values = generator.generate(Config.order.number_of_orders_per_chunk, metric)

		return values

	@timeit
	def __write(self, writer_file_service, values):
		for value in values:
			writer_file_service.write(str(value))

	@timeit
	def __publish(self, serializer, publisher, values):
		for value in values:
			routing_key = value.status.lower().replace(" ", "_")
			value = serializer.serialize(value)
			publisher.publish(RABBITMQ_EXCHANGE, routing_key, value)

	@timeit
	def __read_and_parse_from_file(self, reader_file_service, file_read_seek_number):
		strings_from_file = reader_file_service.read(file_read_seek_number)
		values_from_file = MemoryAllocationManager.get_list()
		for string in strings_from_file:
			value = OrderRecordFromString.get_order_record(string)
			values_from_file.append(value)

		return values_from_file

	@timeit
	def __write_to_db(self, values, db_query_constructor, db_service):
		for value in values:
			query = db_query_constructor.construct(value)
			db_service.execute(query, len(values))

	# reporting function
	def __report(self, logger, program_start_time, metric):
		report_file = Config.file.report_file_path + program_start_time + FILE_EXTENSION_REPORT
		writer_service = FileWriter(logger, report_file, FILE_PERMISSION_REPORT)

		reporter = Reporter(writer_service)
		reporter.report(metric)

	def __finish(self, message_broker_connection_manager, db_connection_manager):
		message_broker_connection_manager.close_connection()
		db_connection_manager.close_connection()

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		program_start_time = str(datetime.now()).replace(":", "-")

		logger, message_broker_connection_manager, db_connection_manager = self.__initialize(program_start_time)
		metric = self.__execute(logger, message_broker_connection_manager, db_connection_manager, program_start_time)
		self.__report(logger, program_start_time, metric)
		self.__finish(message_broker_connection_manager, db_connection_manager)


# Entry point to Data Generator
if __name__ == "__main__":
	launcher = Launcher()
	launcher.launch()
