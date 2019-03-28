from config.config import Config


class Reporter:
	def __init__(self, writer_service):
		self.writer_service = writer_service

	def report(self, gen_time, file_ins_time, message_publish_time, db_exec_time):
		report = self.__construct_report(gen_time, file_ins_time, message_publish_time, db_exec_time)
		self.writer_service.write(report)

	def __construct_report(self, gen_time, file_ins_time, message_publish_time, db_exec_time):
		report = "Startup configurations:\n" +\
				 "Red zone orders: {0}.\n" \
				 "Green zone orders: {1}.\n"\
				 "Blue zone orders: {2}.\n"\
				 "Total orders: {3}.\n"\
				 "Chunk size: {4}.\n"\
				 "----------------------------------\n"\
				 "Results:\n"\
				 "Generation time: {5} ms.\n"\
				 "File insertion time: {6} ms.\n"\
				 "Message publishing time: {7} ms.\n"\
				 "Database insertion time: {8} ms.".format(
					 Config.order.number_of_orders_zone_red,
					 Config.order.number_of_orders_zone_green,
					 Config.order.number_of_orders_zone_blue,
					 Config.order.number_of_orders_total,
					 Config.order.number_of_orders_per_chunk,
					 int(gen_time), int(file_ins_time), int(message_publish_time), int(db_exec_time)
				 )

		return report
