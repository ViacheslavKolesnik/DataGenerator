import time

from service.background_worker.background_worker import BackgroundWorker


class MySQLBackgroundWorker(BackgroundWorker):
	def __init__(self, operation, operation_args, mysql_service, operation_frequency):
		super(MySQLBackgroundWorker, self).__init__(operation, operation_args)
		self.mysql_service = mysql_service
		self.operation_frequency = operation_frequency

		self.stop_flag = False

	def run(self):
		self.mysql_service.open_connection()
		while not self.stop_flag:
			super(MySQLBackgroundWorker, self).run(self.stop_flag)
			time.sleep(self.operation_frequency)
		super(MySQLBackgroundWorker, self).run(self.stop_flag)
		self.mysql_service.close_connection()

	def stop(self):
		self.stop_flag = True
