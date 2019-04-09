from abc import ABC, abstractmethod

from config.config import Config

from utils.utils import Utils


# reporting class
class Reporter(ABC):
	# initialization function
	@abstractmethod
	def __init__(self):
		pass

	# main report function
	@abstractmethod
	def report(self, metric):
		report = self.__construct_report(metric)
		return report

	# construct report from metrics
	def __construct_report(self, metric):
		report = "Startup configurations:\n" \
				 "-Red zone orders: {0}.\n" \
				 "-Green zone orders: {1}.\n"\
				 "-Blue zone orders: {2}.\n"\
				 "-Total orders: {3}.\n"\
				 "-Chunk size: {4}.\n"\
				 "----------------------------------\n"\
				 "Results:\n"\
				 "{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n{11}\n" \
				 "-Written to db:\n" \
				 "{12}\n{13}\n{14}\n{15}\n{16}".format(
					 Config.order.number_of_orders_zone_red,
					 Config.order.number_of_orders_zone_green,
					 Config.order.number_of_orders_zone_blue,
					 Config.order.number_of_orders_total,
					 Config.order.number_of_orders_per_chunk,
					 self.__construct_operation_report("Generation", metric.get_generation()),
					 self.__construct_operation_report("Red zone generation", metric.get_red_zone_order_generation()),
					 self.__construct_operation_report("Green zone generation", metric.get_green_zone_order_generation()),
					 self.__construct_operation_report("Blue zone generation", metric.get_blue_zone_order_generation()),
					 self.__construct_operation_report("Message publishing", metric.get_message_broker_publishing()),
					 self.__construct_operation_report("Database writing", metric.get_database_writing()),
					 "-Received from message broker: {0}".format(metric.get_received_from_message_broker()),
					 "--Order records: {0}".format(metric.get_db_stats()['order_records']),
					 "--Orders: {0}".format(metric.get_db_stats()['orders']),
					 "--Red zone orders: {0}".format(metric.get_db_stats()['red_zone_orders']),
					 "--Green zone orders: {0}".format(metric.get_db_stats()['green_zone_orders']),
					 "--Blue zone orders: {0}".format(metric.get_db_stats()['blue_zone_orders'])
				 )

		return report

	# construct operation report
	# this is used if time metrics for operation were counted
	def __construct_operation_report(self, operation, metrics):
		report = "-{0} time:\n" \
				 "--Max: {1} ms\n" \
				 "--Min: {2} ms\n" \
				 "--Mean: {3} ms\n" \
				 "--Total: {4} ms".format(
			operation,
			Utils.get_max(metrics) if len(metrics) > 0 else "",
			Utils.get_min(metrics) if len(metrics) > 0 else "",
			Utils.get_mean(metrics) if len(metrics) > 0 else "",
			Utils.get_sum(metrics if len(metrics) > 0 else "")
		)

		return report
