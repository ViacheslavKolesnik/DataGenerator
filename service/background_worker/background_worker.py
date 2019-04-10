from threading import Thread
import time


class BackgroundWorker(Thread):
	def __init__(self, operation, operation_frequency, args):
		super(BackgroundWorker, self).__init__()
		self.stop_flag = False
		self.operation = operation
		self.operation_frequency = operation_frequency
		self.args = args

	def run(self):
		while not self.stop_flag:
			self.operation(*self.args)
			time.sleep(self.operation_frequency)

	def stop(self):
		self.stop_flag = True
