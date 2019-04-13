from math import ceil
from datetime import datetime
import time

from config.constant.database import ORDER_RECORD_STATISTICS_SELECT_QUERY, ORDER_RECORD_INSERT_PATTERN
from config.constant.message_broker import *
from config.constant.config import DEFAULT_CONFIG_FILES
from config.constant.other import STORAGE_TO_DB_WRITER_CYCLE_WORK_TIME

from logger.console.console_logger import ConsoleLogger
from logger.provider.logger_provider import LoggerProvider
from config.parser.ini.ini_config_parser import INIConfigurationParser
from config.config import Config
from reporter.provider.reporter_provider import ReporterProvider
from service.background_worker.mysql.mysql_periodic_worker import MySQLPeriodicBackgroundWorker
from service.background_worker.mysql.mysql_worker import MySQLBackgroundWorker
from service.message_broker.rabbitmq.broker import RabbitMQ
from utils.utils import Utils
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from generator.order.order_generator import OrderGenerator
from serializer.order_record.serializer import OrderRecordSerializer
from service.database.query_constructor.order_record.query_constructor import OrderRecordDBQueryConstructor
from service.database.mysql.mysql_service import MySQLService
from metric.generator.order_generator.metric import OrderGeneratorMetric
from metric.decorator.metric_decorator import timeit
from service.storage.storage import Storage


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
		logger.info("Logger initialized. Initializing data generator.")

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

		logger.info("Initializing message broker.")
		message_broker = RabbitMQ(logger,
								  user=Config.message_broker.user,
								  password=Config.message_broker.password,
								  host=Config.message_broker.host,
								  virtual_host=Config.message_broker.virtual_host,
								  port=Config.message_broker.port)
		logger.info("Opening message broker connection.")
		message_broker.open_connection()

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
		message_broker.add_consumer(storage, RABBITMQ_QUEUE_NEW)
		message_broker.add_consumer(storage, RABBITMQ_QUEUE_TO_PROVIDER)
		message_broker.add_consumer(storage, RABBITMQ_QUEUE_FINAL)
		logger.info("Starting consumers.")
		message_broker.start_consumers()

		logger.info("Initializing database service.")
		db_service = MySQLService(logger,
								  user=Config.database.user,
								  password=Config.database.password,
								  host=Config.database.host,
								  port=Config.database.port,
								  database_name=Config.database.database_name)
		logger.info("Establishing database connection.")
		db_service.open_connection()

		logger.info("Initializing reporter.")
		reporter = ReporterProvider.get_reporter(Config.report.report_output, program_start_time, logger)

		logger.info("Initializing metrics.")
		metric = OrderGeneratorMetric()

		logger.info("Starting background reporting every {0} seconds".format(Config.report.report_frequency))
		background_reporter = MySQLPeriodicBackgroundWorker(self.__report, (logger, reporter, metric, db_service, storage), db_service, Config.report.report_frequency)
		background_reporter.start()

		logger.info("Starting background database writer")
		db_query_constructor = OrderRecordDBQueryConstructor()
		serializer = OrderRecordSerializer()
		background_db_writer = MySQLBackgroundWorker(self.__storage_to_db_writer, (storage, logger, serializer, db_query_constructor, db_service, metric), db_service)
		background_db_writer.start()

		return logger, reporter, background_reporter, background_db_writer, metric, message_broker, storage, db_service, serializer

	# main execution function
	def __execute(self, logger, metric, message_broker, serializer):
		generator = OrderGenerator(logger)

		generated_values = 0

		for iterator in range(int(ceil(Config.order.number_of_orders_total / Config.order.number_of_orders_per_chunk))):
			logger.info("Generating values.")
			values = self.__generate(logger, generator, metric, metrics=metric.get_generation())
			generated_values += len(values)

			logger.info("Publishing values.")
			self.__publish(logger, serializer, message_broker.publishers, values, metrics=metric.get_message_broker_publishing())

		logger.info("Generated {0} values.".format(generator.total_number_of_generated_values))

		return metric

	def __storage_to_db_writer(self, storage, logger, serializer, db_query_constructor, db_service, metric):
		while True:
			number_of_stored_values = storage.get_amount_stored()
			number_of_extracted_from_storage_values = storage.get_number_of_extracted()
			if number_of_stored_values == 0 and number_of_extracted_from_storage_values > 0:
				break
			elif number_of_stored_values > 0:
				values = storage.get(number_of_stored_values)
				write_to_db_success = self.__write_to_db(logger, serializer, values, db_query_constructor, db_service, metrics=metric.get_database_writing())

				if write_to_db_success:
					storage.delete(number_of_stored_values)

			time.sleep(STORAGE_TO_DB_WRITER_CYCLE_WORK_TIME)


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
			query = db_query_constructor.construct(ORDER_RECORD_INSERT_PATTERN, value)
			query_execution_success = db_service.execute(query, len(values))
			if query_execution_success:
				written_to_db_values_number += 1
			else:
				return False
		logger.debug("Written {0} values to db.".format(written_to_db_values_number))
		return True

	def __prepare_for_final_report(self, logger, background_reporter, background_db_writer):
		logger.info("Stopping background reporter.")
		background_reporter.stop()
		logger.info("Waiting for background reporter to stop.")
		background_reporter.join()
		logger.info("Waiting for background database writer to stop.")
		background_db_writer.join()

	# reporting function
	def __report(self, logger, reporter, metric, db_service, storage):
		metric.set_received_from_message_broker(storage.get_number_put())
		db_stats = db_service.execute_select(ORDER_RECORD_STATISTICS_SELECT_QUERY)
		if not db_stats:
			logger.warn("Unable to write report, data from database is not available.")
			return
		db_stats = db_stats[0]
		metric.set_db_stats(db_stats)

		reporter.report(metric)

	def __finish(self, logger, message_broker, db_service):
		logger.info("Closing database connection.")
		db_service.close_connection()
		logger.info("Stopping consumers.")
		message_broker.stop_consumers()
		logger.info("Waiting for consumers to stop.")
		for consumer in message_broker.consumers:
			consumer.join()
		logger.info("Closing message broker connection.")
		message_broker.close_connection()

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		program_start_time = str(datetime.now()).replace(":", "-")

		logger,\
		reporter,\
		background_reporter,\
		background_db_writer,\
		metric,\
		message_broker,\
		storage,\
		db_service,\
		serializer = self.__initialize(program_start_time)

		logger.info("Starting data generator execution.")
		metric = self.__execute(logger, metric, message_broker, serializer)
		logger.info("Preparing for final report.")
		self.__prepare_for_final_report(logger, background_reporter, background_db_writer)
		logger.info("Writing final report.")
		self.__report(logger, reporter, metric, db_service, storage)
		logger.info("Finishing data generator.")
		self.__finish(logger, message_broker, db_service)
