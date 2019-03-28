from datetime import datetime

from config.constant.file import FILE_PATH_LOG, FILE_EXTENSION_LOG, FILE_PERMISSION_LOG
from config.constant.exit_code import EXIT_CODE_UNKNOWN_ERROR, EXIT_CODE_FILE_ERROR

from logger.logger import Logger


# logging class
# log_file - file for writing log
# log_file_permission - permission for log file
class FileLogger(Logger):
	# initialization method
	# setting log file
	# setting log file permission
	def __init__(self):
		super(FileLogger, self).__init__()

		self.log_file = FILE_PATH_LOG + str(datetime.now()) + FILE_EXTENSION_LOG
		self.log_file_permission = FILE_PERMISSION_LOG

	# general log writing function
	def _Logger__write_log(self, log_class, message):
		time = datetime.now()
		log = "{0} [{1}]: {2}\n".format(str(time), log_class, message)
		try:
			with open(self.log_file, self.log_file_permission) as log_file:
				log_file.write(log)
		except IOError:
			print("IOError. Unable to write log.")
			exit(EXIT_CODE_FILE_ERROR)
		except:
			print("Error. Unable to write log.")
			exit(EXIT_CODE_UNKNOWN_ERROR)
