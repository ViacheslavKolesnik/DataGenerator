from abc import ABCMeta, abstractmethod

from config.constant.log import LOG_INFO, LOG_ERROR, LOG_FATAL

from logger.log_level import LogLevel


# logging abstract class
# info_enabled - info log switcher
# error_enabled - error log switcher
class Logger:
	__metaclass__ = ABCMeta

	# initialization function
	@abstractmethod
	def __init__(self):
		self.log_level = LogLevel.INFO.value

	# setting log levels
	def set_log_level(self, log_level):
		self.log_level = log_level

	# general log writing function
	# abstract method
	# class method
	# needs to be overridden
	@abstractmethod
	def __write_log(self, log_class, message):
		pass

	# info log constructing function
	def debug(self, message):
		if self.log_level <= LogLevel.DEBUG.value:
			self.__write_log(LogLevel.DEBUG.name, message)

	# info log constructing function
	def info(self, message):
		if self.log_level <= LogLevel.INFO.value:
			self.__write_log(LogLevel.INFO.name, message)

	# info log constructing function
	def warn(self, message):
		if self.log_level <= LogLevel.WARN.value:
			self.__write_log(LogLevel.WARN.name, message)

	# error log constructing function
	def error(self, message):
		if self.log_level <= LogLevel.ERROR.value:
			self.__write_log(LogLevel.ERROR.name, message)

	# fatal log constructing function
	def fatal(self, message):
		self.__write_log(LogLevel.FATAL.name, message)
