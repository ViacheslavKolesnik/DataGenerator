from __future__ import division

from math import ceil
from datetime import datetime

from config.constant.file import *
from config.constant.message_broker import RABBITMQ_EXCHANGE
from config.constant.other import SECOND_TO_MICROSECOND_CONVERTING_COEF

from logger.file_logger.file_logger import FileLogger
from config.config_parser import ConfigurationParser
from config.config import Config
from utils.utils import Utils
from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from generator.order.order_generator import OrderGenerator
from service.file_service.writer.order_record.order_record_file_writer import OrderRecordFileWriter
from service.file_service.writer.message.message_file_writer import MessageFileWriter
from service.file_service.reader.reader_file_service import ReaderFileService
from serializer.order_record.string_serializer import OrderRecordStringSerializer
from service.message_broker.connection_manager.rabbitmq.rabbitmq_connection_manager import RabbitMQConnectionManager
from service.message_broker.publisher.rabbitmq.rrabbitmq_publisher import RabbitMQPublisher
from serializer.order_record.db_serializer import OrderRecordDataBaseSerializer
from service.database.connection_manager.mysql.mysql_connection_manager import MySQLConnectionManager
from service.database.service.mysql.mysql_service import MySQLService
from reporter.reporter import Reporter


# main program class
# handles program execution
class Launcher:
	# main initializing function of Data Generator
	# initialize logger
	# initialize utils
	# initialize memory allocation manager
	# parse configurations
	# initialize generator
	def __initialize(self):
		logger = FileLogger()
		logger.info("Logger initialized. Initializing data generator.")

		logger.info("Initializing utils.")
		Utils.initialize(logger)

		logger.info("Initializing memory allocation manager.")
		MemoryAllocationManager.initialize(logger)

		logger.info("Parsing config files.")
		ConfigurationParser(logger).parse_config()

		logger.info("Setting log level.")
		logger.set_log_level(Config.log.log_level)

		return logger

	# main execution function
	def __execute(self, logger):
		logger.info("Initializing generator.")
		generator = OrderGenerator(logger)

		logger.info("Initializing writer file service.")
		writer_file_service = OrderRecordFileWriter(logger, Config.file.data_output_file, FILE_PERMISSION_DATA_OUTPUT)
		logger.info("Initializing reader file service.")
		reader_file_service = ReaderFileService(logger, Config.file.data_output_file, FILE_PERMISSION_READ_DATA_OUTPUT)

		logger.info("Starting data generator.")

		string_serializer = OrderRecordStringSerializer(logger)
		message_broker_connection_manager = RabbitMQConnectionManager(logger,
													   user=Config.message_broker.user,
													   password=Config.message_broker.password,
													   host=Config.message_broker.host,
													   virtual_host=Config.message_broker.virtual_host,
													   port=Config.message_broker.port)
		publisher = RabbitMQPublisher(message_broker_connection_manager)

		db_serializer = OrderRecordDataBaseSerializer(logger)
		db_connection_manager = MySQLConnectionManager(logger,
													   user=Config.database.user,
													   password=Config.database.password,
													   host=Config.database.host,
													   port=Config.database.port,
													   database_name=Config.database.database_name)
		db_service = MySQLService(logger, db_connection_manager)

		gen_time = 0
		file_ins_time = 0
		message_publish_time = 0
		db_exec_time = 0

		for iterator in range(int(ceil(Config.order.number_of_orders_total / Config.order.number_of_orders_per_chunk))):
			gen_start = datetime.now()
			values = generator.generate(Config.order.number_of_orders_per_chunk)
			gen_finish = datetime.now()
			gen_time += (gen_finish - gen_start).total_seconds() * SECOND_TO_MICROSECOND_CONVERTING_COEF

			file_ins_start = datetime.now()
			writer_file_service.write(values)
			file_ins_finish = datetime.now()
			file_ins_time += (file_ins_finish - file_ins_start).total_seconds() * SECOND_TO_MICROSECOND_CONVERTING_COEF

			message_publish_start = datetime.now()
			publisher.publish_multiple(RABBITMQ_EXCHANGE, values, string_serializer)
			message_publish_finish = datetime.now()
			message_publish_time += (message_publish_finish - message_publish_start).total_seconds() * SECOND_TO_MICROSECOND_CONVERTING_COEF

			values_from_file = reader_file_service.read()

			db_exec_start = datetime.now()
			db_service.execute_multiple(values_from_file, db_serializer)
			db_exec_finish = datetime.now()
			db_exec_time += (db_exec_finish - db_exec_start).total_seconds() * SECOND_TO_MICROSECOND_CONVERTING_COEF

		logger.info("Generated {0} values.".format(generator.total_number_of_generated_values))

		return gen_time, file_ins_time, message_publish_time, db_exec_time

	# reporting function
	def __report(self, logger, gen_time, file_ins_time, message_publish_time, db_exec_time):
		report_start_time = datetime.now()
		report_file = Config.file.report_file_path + str(report_start_time) + FILE_EXTENSION_REPORT
		writer_service = MessageFileWriter(logger, report_file, FILE_PERMISSION_REPORT)

		reporter = Reporter(writer_service)
		reporter.report(gen_time, file_ins_time, message_publish_time, db_exec_time)

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		logger = self.__initialize()
		gen_time, file_ins_time, message_publish_time, db_exec_time = self.__execute(logger)
		self.__report(logger, gen_time, file_ins_time, message_publish_time, db_exec_time)


# Entry point to Data Generator
if __name__ == "__main__":
	launcher = Launcher()
	launcher.launch()
