from datetime import datetime

from logger.logger import Logger


# logging class
# log_file - file for writing log
# log_file_permission - permission for log file
class ConsoleLogger(Logger):
	# initialization method
	# setting log file
	# setting log file permission
	def __init__(self):
		super(ConsoleLogger, self).__init__()

	# general log writing function
	def _Logger__write_log(self, log_class, message):
		time = datetime.now()
		log = "{0} [{1}]: {2}\n".format(str(time), log_class, message)
		print(log, end='')
