from threading import Thread
import time


class BackgroundWorker(Thread):
	def __init__(self, operation_frequency, operation, operation_args):
		super(BackgroundWorker, self).__init__()
		self.stop_flag = False
		self.operation_frequency = operation_frequency
		self.operation = operation
		self.operation_args = operation_args

	def run(self):
		while not self.stop_flag:
			self.operation(*self.operation_args)
			time.sleep(self.operation_frequency)

	def stop(self):
		self.stop_flag = True
