from config.config import Config

from utils.utils import Utils

class Reporter:
	def __init__(self, writer_service):
		self.writer_service = writer_service

	def report(self, metric):
		report = self.__construct_report(metric)
		self.writer_service.write(report)

	def __construct_report(self, metric):
		report = "Startup configurations:\n" \
				 "-Red zone orders: {0}.\n" \
				 "-Green zone orders: {1}.\n"\
				 "-Blue zone orders: {2}.\n"\
				 "-Total orders: {3}.\n"\
				 "-Chunk size: {4}.\n"\
				 "----------------------------------\n"\
				 "Results:\n"\
				 "{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n{11}\n{12}".format(
					 Config.order.number_of_orders_zone_red,
					 Config.order.number_of_orders_zone_green,
					 Config.order.number_of_orders_zone_blue,
					 Config.order.number_of_orders_total,
					 Config.order.number_of_orders_per_chunk,
					 self.__construct_operation_report("Generation", metric.get_generation()),
					 self.__construct_operation_report("Red zone generation", metric.get_red_zone_order_generation()),
					 self.__construct_operation_report("Green zone generation", metric.get_green_zone_order_generation()),
					 self.__construct_operation_report("Blue zone generation", metric.get_blue_zone_order_generation()),
					 self.__construct_operation_report("File insertion", metric.get_file_insertion()),
					 self.__construct_operation_report("Message publishing", metric.get_message_broker_publishing()),
					 self.__construct_operation_report("File reading and parsing", metric.get_file_reading_and_parsing()),
					 self.__construct_operation_report("Database writing", metric.get_database_writing())
				 )

		return report

	def __construct_operation_report(self, operation, metrics):
		report = "-{0} time:\n" \
				 "--Max: {1} ms\n" \
				 "--Min: {2} ms\n" \
				 "--Mean: {3} ms\n" \
				 "--Total: {4} ms".format(
			operation,
			Utils.get_max(metrics),
			Utils.get_min(metrics),
			Utils.get_mean(metrics),
			Utils.get_sum(metrics)
		)

		return report
