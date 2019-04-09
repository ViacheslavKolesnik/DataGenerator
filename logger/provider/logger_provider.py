from config.constant.log import LOG_OUTPUT_FILE, LOG_OUTPUT_CONSOLE

from logger.console.console_logger import ConsoleLogger
from logger.file.file_logger import FileLogger


# class for providing loggers
class LoggerProvider:
	# log_output - log output type
	# program_start_time - the time program has started at
	# return logger depending on log output type
	@staticmethod
	def get_logger(log_output=LOG_OUTPUT_CONSOLE, program_start_time=None):
		if log_output == LOG_OUTPUT_FILE:
			if program_start_time is not None:
				return FileLogger(program_start_time)
			else:
				print("Error. Cannot instantiate FileLogger. No program_start_time specified. Using ConsoleLogger.")
				return ConsoleLogger()
		else:
			return ConsoleLogger()
