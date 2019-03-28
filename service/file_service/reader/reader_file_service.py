from google.protobuf.internal.decoder import _DecodeVarint32

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from service.file_service.file_service import FileService
from generator.order.entities.order_record_pb2 import OrderRecord


# service for writing to file
class ReaderFileService(FileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		super(ReaderFileService, self).__init__(logger, file_string, permission)

	# write messages to file
	# messages - list of messages
	# serializer - messages serializer
	# if serializer specified serialize messages then write to file
	def read(self):
		number_of_read_messages = 0
		records = MemoryAllocationManager.get_list()

		try:
			with open(self.file_string, self.permission) as file:
				buffer = file.read()
				cursor = 0
				while cursor < len(buffer):
					message_length, new_position = _DecodeVarint32(buffer, cursor)
					cursor = new_position
					msg_buf = buffer[cursor:cursor+message_length]
					cursor += message_length

					record = OrderRecord()
					record.ParseFromString(msg_buf)

					records.append(record)
					number_of_read_messages += 1
		except IOError as e:
			self.logger.error("IOError occured while reading from file.")
			self.logger.error(str(e))
		except:
			self.logger.error("Error occured while reading from file.")

		self.logger.info("Read {0} messages from file.".format(number_of_read_messages))
		return records
