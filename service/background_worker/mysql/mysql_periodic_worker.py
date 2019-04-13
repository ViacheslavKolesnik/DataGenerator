import time

from service.background_worker.background_worker import BackgroundWorker


class MySQLPeriodicBackgroundWorker(BackgroundWorker):
	def __init__(self, operation, operation_args, mysql_service, operation_frequency):
		super(MySQLPeriodicBackgroundWorker, self).__init__(operation, operation_args)
		self.operation_frequency = operation_frequency
		self.mysql_service = mysql_service

		self.stop_flag = False

	def run(self):
		self.mysql_service.open_connection()
		while not self.stop_flag:
			super(MySQLPeriodicBackgroundWorker, self).run()
			time.sleep(self.operation_frequency)
		self.mysql_service.close_connection()

	def stop(self):
		self.stop_flag = True
