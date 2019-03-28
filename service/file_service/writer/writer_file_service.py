from abc import ABC, abstractmethod

from service.file_service.file_service import FileService


# service for writing to file
class WriterFileService(FileService):
	# initialization function
	# set logger, file string and file permission
	@abstractmethod
	def __init__(self, logger, file_string, permission):
		super(WriterFileService, self).__init__(logger, file_string, permission)

	# write to file
	@abstractmethod
	def write(self, *args):
		pass
