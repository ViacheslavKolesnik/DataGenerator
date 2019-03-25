from abc import ABCMeta, abstractmethod
from config.constants.constants_log import LOG_INFO, LOG_ERROR, LOG_FATAL


# logging abstract class
# info_enabled - info log switcher
# error_enabled - error log switcher
class Logger:
	__metaclass__ = ABCMeta

	# initialization function
	@abstractmethod
	def __init__(self):
		self.info_enabled = True
		self.error_enabled = True

	# setting log levels
	def set_log_levels(self, info_enabled, error_enabled):
		self.info_enabled = info_enabled
		self.error_enabled = error_enabled

	# general log writing function
	# abstract method
	# class method
	# needs to be overridden
	@abstractmethod
	def __write_log(self, log_class, message):
		pass

	# info log constructing function
	def info(self, message):
		if self.info_enabled:
			self.__write_log(LOG_INFO, message)

	# error log constructing function
	def error(self, message):
		if self.error_enabled:
			self.__write_log(LOG_ERROR, message)

	# fatal log constructing function
	def fatal(self, message):
		self.__write_log(LOG_FATAL, message)
