from service.file_service.writer.writer_file_service import WriterFileService
from google.protobuf.internal.encoder import _VarintBytes


# service for writing to file
class MessageFileWriter(WriterFileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		super(WriterFileService, self).__init__(logger, file_string, permission)

	# write messages to file
	# messages - list of messages
	# serializer - messages serializer
	# if serializer specified serialize messages then write to file
	def write(self, message):
		try:
			with open(self.file_string, self.permission) as file:
				file.write(message)
		except IOError as e:
			self.logger.error("IOError occured while writing to file.")
			self.logger.error(str(e))
		except:
			self.logger.error("Error occured while writing to file.")

