from math import ceil
from datetime import datetime

from config.constant.file import *
from config.constant.message_broker import RABBITMQ_EXCHANGE
from config.constant.config import DEFAULT_CONFIG_FILES

from logger.console.console_logger import ConsoleLogger
from logger.provider.logger_provider import LoggerProvider
from config.parser.ini.ini_config_parser import INIConfigurationParser
from config.config import Config
from reporter.provider.reporter_provider import ReporterProvider
from service.message_broker.rabbitmq.broker import RabbitMQ
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
		logger = ConsoleLogger()
		logger.info("Logger initialized. Initializing data order_generator.")

		logger.info("Initializing utils.")
		Utils.initialize(logger)

		logger.info("Initializing memory allocation manager.")
		MemoryAllocationManager.initialize(logger)

		logger.info("Parsing config files.")
		INIConfigurationParser(logger, DEFAULT_CONFIG_FILES).parse_config()

		logger.info("Resetting logger.")
		logger = LoggerProvider.get_logger(Config.log.log_output, program_start_time)
		logger.info("Setting log level.")
		logger.set_log_level(Config.log.log_level)

		logger.info("Establishing message broker connection.")
		message_broker_connection_manager = RabbitMQConnectionManager(logger,
													   user=Config.message_broker.user,
													   password=Config.message_broker.password,
													   host=Config.message_broker.host,
													   virtual_host=Config.message_broker.virtual_host,
													   port=Config.message_broker.port)
		message_broker_connection_manager.open_connection()

		logger.info("Setting up message broker.")
		channel = message_broker_connection_manager.get_channel()
		message_broker = RabbitMQ(logger, channel)
		message_broker.setup()
		message_broker_connection_manager.close_channel(channel)

		logger.info("Establishing database connection.")
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
			logger.info("Generating values.")
			values = self.__generate(logger, generator, metric, metrics=metric.get_generation())

			logger.info("Writing values.")
			self.__write(logger, writer_file_service, values, metrics=metric.get_file_insertion())

			logger.info("Publishing values.")
			self.__publish(logger, serializer, publisher, values, metrics=metric.get_message_broker_publishing())

			logger.info("Reading values.")
			values_from_file = self.__read_and_parse_from_file(logger, reader_file_service, file_read_seek_number, metrics=metric.get_file_reading_and_parsing())
			file_read_seek_number += len(values_from_file)

			logger.info("Writing values to database.")
			self.__write_to_db(logger, values, db_query_constructor, db_service, metrics=metric.get_database_writing())

		logger.info("Generated {0} values.".format(generator.total_number_of_generated_values))

		return metric

	@timeit
	def __generate(self, logger, generator, metric):
		values = generator.generate(Config.order.number_of_orders_per_chunk, metric)
		logger.debug("Generated {0} values.".format(len(values)))

		return values

	@timeit
	def __write(self, logger, writer_file_service, values):
		written_values_number = 0
		for value in values:
			writer_file_service.write(str(value))
			written_values_number += 1
		logger.debug("Written {0} values.".format(written_values_number))

	@timeit
	def __publish(self, logger, serializer, publisher, values):
		published_values_number = 0
		for value in values:
			routing_key = value.status.lower().replace(" ", "_")
			value = serializer.serialize(value)
			publisher.publish(RABBITMQ_EXCHANGE, routing_key, value)
			published_values_number += 1
		logger.debug("Published {0} values.".format(published_values_number))

	@timeit
	def __read_and_parse_from_file(self, logger, reader_file_service, file_read_seek_number):
		strings_from_file = reader_file_service.read(file_read_seek_number)
		values_from_file = MemoryAllocationManager.get_list()
		read_values_number = 0
		for string in strings_from_file:
			value = OrderRecordFromString.get_order_record(string)
			values_from_file.append(value)
			read_values_number += 1
		logger.debug("Read {0} values.".format(read_values_number))

		return values_from_file

	@timeit
	def __write_to_db(self, logger, values, db_query_constructor, db_service):
		written_to_db_values_number = 0
		for value in values:
			query = db_query_constructor.construct(value)
			db_service.execute(query, len(values))
			written_to_db_values_number += 1
		logger.debug("Written {0} values to db.".format(written_to_db_values_number))

	# reporting function
	def __report(self, logger, program_start_time, metric):
		reporter = ReporterProvider.get_reporter(Config.report.report_output, program_start_time, logger)
		reporter.report(metric)

	def __finish(self, logger, message_broker_connection_manager, db_connection_manager):
		logger.info("Closing message broker connection.")
		message_broker_connection_manager.close_connection()
		logger.info("Closing database connection.")
		db_connection_manager.close_connection()

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		program_start_time = str(datetime.now()).replace(":", "-")

		logger, message_broker_connection_manager, db_connection_manager = self.__initialize(program_start_time)
		logger.info("Starting data generator execution.")
		metric = self.__execute(logger, message_broker_connection_manager, db_connection_manager, program_start_time)
		logger.info("Writing report.")
		self.__report(logger, program_start_time, metric)
		logger.info("Finishing data generator.")
		self.__finish(logger, message_broker_connection_manager, db_connection_manager)
