from google.protobuf.internal.decoder import _DecodeVarint32

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from service.file_service.file_service import FileService
from generator.order.entities.order_record import OrderRecord


# service for writing to file
class ReaderFileService(FileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		super(ReaderFileService, self).__init__(logger, file_string, permission)

	# write messages to file
	# messages - list of messages
	# serializer - messages serializer
	# if serializer specified construct messages then write to file
	def read(self, seek_number):
		lines = None

		try:
			with open(self.file_string, self.permission) as file:
				lines = file.readlines()
				lines = lines[seek_number:]
		except IOError as e:
			self.logger.error("IOError occured while reading from file.")
			self.logger.error(str(e))
		except:
			self.logger.error("Error occured while reading from file.")

		return lines
