from service.background_worker.background_worker import BackgroundWorker


class MySQLBackgroundWorker(BackgroundWorker):
	def __init__(self, operation_frequency, operation, operation_args, mysql_service):
		super(MySQLBackgroundWorker, self).__init__(operation_frequency, operation, operation_args)
		self.mysql_service = mysql_service

	def run(self):
		self.mysql_service.open_connection()
		super(MySQLBackgroundWorker, self).run()
		self.mysql_service.close_connection()

	def stop(self):
		super(MySQLBackgroundWorker, self).stop()
