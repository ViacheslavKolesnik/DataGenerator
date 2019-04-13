from threading import Thread


class BackgroundWorker(Thread):
	def __init__(self, operation, operation_args, *args, **kwargs):
		super(BackgroundWorker, self).__init__()
		self.operation = operation
		self.operation_args = operation_args

	def run(self):
		self.operation(*self.operation_args)
