from abc import ABCMeta, abstractmethod


# class for working with files
class FileService:
	__metaclass__ = ABCMeta

	# initialization function
	# file - file
	# permission - file permission
	# connection - file connection
	@abstractmethod
	def __init__(self, logger, file_string, permission):
		self.logger = logger
		self.file_string = file_string
		self.permission = permission
