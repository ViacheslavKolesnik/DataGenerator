from datetime import datetime

from logger.logger import Logger


# console logging class
class ConsoleLogger(Logger):
	# initialization method
	def __init__(self):
		super(ConsoleLogger, self).__init__()

	# general log writing function
	def _Logger__write_log(self, log_class, message):
		time = datetime.now()
		log = "{0} [{1}]: {2}\n".format(str(time), log_class, message)
		print(log, end='')
