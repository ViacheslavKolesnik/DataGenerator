import threading
import time
from math import ceil
from datetime import datetime

from config.constant.database import ORDER_RECORD_STATISTICS_SELECT_QUERY, DISABLE_SQL_MODE_ONLY_FULL_GROUP_BY
from config.constant.file import *
from config.constant.message_broker import *
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
from service.file_service.writer.csv_writer import CSVFileWriter
from service.file_service.reader.csv_reader import CSVFileReader
from serializer.order_record.serializer import OrderRecordSerializer
from service.message_broker.connection_manager.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager
from service.database.query_constructor.order_record.query_constructor import OrderRecordDBQueryConstructor
from service.database.connection_manager.mysql.mysql_connection_manager import MySQLConnectionManager
from service.database.service.mysql.mysql_service import MySQLService
from metric.generator.order_generator.metric import OrderGeneratorMetric
from metric.decorator.metric_decorator import timeit
from service.storage.storage import Storage
from service.background_worker.background_worker import BackgroundWorker


# main program class
# handles program execution
class Launcher:
	# main initializing function of Data Generator
	# initialize logger
	# initialize utils
	# initialize memory allocation manager
	# parse configurations
	# reset logger according to configurations
	# initialize message broker connection manager
	# initialize database connection manager
	# establish database connection
	# initialize database service
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

		logger.info("Initializing storage for consumed messages.")
		storage = Storage()

		logger.info("Initializing message broker connection manager.")
		message_broker_connection_manager = RabbitMQConnectionManager(logger,
													   user=Config.message_broker.user,
													   password=Config.message_broker.password,
													   host=Config.message_broker.host,
													   virtual_host=Config.message_broker.virtual_host,
													   port=Config.message_broker.port)

		logger.info("Opening message broker connection.")
		message_broker_general_connection = message_broker_connection_manager.open_connection()
		logger.info("Initializing message broker.")
		message_broker = RabbitMQ(logger, message_broker_general_connection)
		logger.info("Adding message broker publishers.")
		message_broker.add_publisher(RABBITMQ_EXCHANGE,
													 RABBITMQ_EXCHANGE_TYPE,
													 RABBITMQ_QUEUE_NEW,
													 [RABBITMQ_QUEUE_BIND_ROUTING_KEY_NEW])
		message_broker.add_publisher(RABBITMQ_EXCHANGE,
															 RABBITMQ_EXCHANGE_TYPE,
															 RABBITMQ_QUEUE_TO_PROVIDER,
															 [RABBITMQ_QUEUE_BIND_ROUTING_KEY_TO_PROVIDER])
		message_broker.add_publisher(RABBITMQ_EXCHANGE,
													   RABBITMQ_EXCHANGE_TYPE,
													   RABBITMQ_QUEUE_FINAL,
													   [RABBITMQ_QUEUE_BIND_ROUTING_KEY_FILLED,
														RABBITMQ_QUEUE_BIND_ROUTING_KEY_PARTIAL_FILLED,
														RABBITMQ_QUEUE_BIND_ROUTING_KEY_REJECTED])
		logger.info("Adding message broker consumers.")
		message_broker.add_consumer(message_broker_connection_manager, storage, RABBITMQ_QUEUE_NEW)
		message_broker.add_consumer(message_broker_connection_manager, storage, RABBITMQ_QUEUE_TO_PROVIDER)
		message_broker.add_consumer(message_broker_connection_manager, storage, RABBITMQ_QUEUE_FINAL)
		logger.info("Starting consumers.")
		message_broker.start_consumers()

		logger.info("Initializing database connection manager.")
		db_connection_manager = MySQLConnectionManager(logger,
													   user=Config.database.user,
													   password=Config.database.password,
													   host=Config.database.host,
													   port=Config.database.port,
													   database_name=Config.database.database_name)
		logger.info("Establishing database connection.")
		db_connection = db_connection_manager.open_connection()

		logger.info("Initializing database service.")
		db_service = MySQLService(logger, db_connection)

		logger.info("Initializing reporter.")
		reporter = ReporterProvider.get_reporter(Config.report.report_output, program_start_time, logger)

		logger.info("Initializing metrics.")
		metric = OrderGeneratorMetric()

		reporter_db_connection = db_connection_manager.open_connection()
		reporter_db_service = MySQLService(logger, reporter_db_connection)
		reporter_db_service.execute(DISABLE_SQL_MODE_ONLY_FULL_GROUP_BY, 1)
		logger.info("Starting background reporting every {0} seconds".format(Config.report.report_frequency))
		background_reporter = BackgroundWorker(self.__report, Config.report.report_frequency, (reporter, metric, reporter_db_service))
		background_reporter.start()

		return logger, reporter, background_reporter, metric, message_broker_connection_manager, message_broker, storage, db_connection_manager, db_service

	# main execution function
	def __execute(self, logger, metric, message_broker, storage, db_connection_manager, db_service):
		generator = OrderGenerator(logger)

		serializer = OrderRecordSerializer()

		db_query_constructor = OrderRecordDBQueryConstructor()

		generated_values = 0
		chunks = MemoryAllocationManager.get_list()

		for iterator in range(int(ceil(Config.order.number_of_orders_total / Config.order.number_of_orders_per_chunk))):
			logger.info("Generating values.")
			values = self.__generate(logger, generator, metric, metrics=metric.get_generation())
			generated_values += len(values)
			chunks.append(len(values))

			logger.info("Publishing values.")
			self.__publish(logger, serializer, message_broker.publishers, values, metrics=metric.get_message_broker_publishing())

		logger.info("Generated {0} values.".format(generator.total_number_of_generated_values))

		while generated_values != storage.get_number_of_extracted():
			if len(chunks) > 0 and storage.get_amount_stored() >= chunks[0]:
				values = storage.get(chunks[0])
				write_to_db_success = self.__write_to_db(logger, serializer, values, db_query_constructor, db_service, metrics=metric.get_database_writing())
				if write_to_db_success:
					storage.delete(chunks[0])
					del chunks[:1]
				else:
					db_connection_manager.open_connection()
					db_service.connection = db_connection_manager.connection
			else:
				break

		metric.set_received_from_message_broker(storage.get_number_put())

		return metric

	@timeit
	def __generate(self, logger, generator, metric):
		values = generator.generate(Config.order.number_of_orders_per_chunk, metric)
		logger.debug("Generated {0} values.".format(len(values)))

		return values

	@timeit
	def __publish(self, logger, serializer, publishers, values):
		published_values_number = 0
		for value in values:
			routing_key = value.status.lower().replace(" ", "_")
			value = serializer.serialize(value)
			for publisher in publishers:
				if routing_key in publisher.routing_keys:
					publisher.publish(routing_key, value)
					break
			published_values_number += 1
		logger.debug("Published {0} values.".format(published_values_number))


	@timeit
	def __write_to_db(self, logger, serializer, values, db_query_constructor, db_service):
		written_to_db_values_number = 0
		for value in values:
			value = serializer.deserialize(value)
			query = db_query_constructor.construct(value)
			query_execution_success = db_service.execute(query, len(values))
			if query_execution_success:
				written_to_db_values_number += 1
			else:
				return False
		logger.debug("Written {0} values to db.".format(written_to_db_values_number))
		return True

	# reporting function
	def __report(self, reporter, metric, db_service):
		db_stats = db_service.execute_select(ORDER_RECORD_STATISTICS_SELECT_QUERY)
		db_stats = db_stats[0]
		metric.set_db_stats(db_stats)

		reporter.report(metric)

	def __finish(self, logger, message_broker, message_broker_connection_manager, db_connection_manager, background_reporter):
		logger.info("Stopping background reporter.")
		background_reporter.stop()
		logger.info("Stopping consumers.")
		message_broker.stop_consumers()
		logger.info("Closing message broker connection.")
		message_broker_connection_manager.close_connection(message_broker.connection)
		logger.info("Closing database connection.")
		db_connection_manager.close_all_connections()

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		program_start_time = str(datetime.now()).replace(":", "-")

		logger,\
		reporter, \
		background_reporter,\
		metric,\
		message_broker_connection_manager,\
		message_broker,\
		storage,\
		db_connection_manager,\
		db_service = self.__initialize(program_start_time)

		logger.info("Starting data generator execution.")
		metric = self.__execute(logger, metric, message_broker, storage, db_connection_manager, db_service)
		logger.info("Writing report.")
		self.__report(reporter, metric, db_service)
		logger.info("Finishing data generator.")
		self.__finish(logger, message_broker, message_broker_connection_manager, db_connection_manager, background_reporter)
