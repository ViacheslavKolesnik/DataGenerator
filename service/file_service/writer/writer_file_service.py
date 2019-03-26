from service.file_service.file_service import FileService


# service for writing to file
class WriterFileService(FileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		super(WriterFileService, self).__init__(logger, file_string, permission)

	# write messages to file
	# messages - list of messages
	# serializer - messages serializer
	# if serializer specified serialize messages then write to file
	def write(self, messages, serializer=None):
		serialized_messages = messages
		number_of_written_messages = 0

		try:
			if serializer is not None:
				serialized_messages = serializer.serialize(messages)
			with open(self.file_string, self.permission) as file:
				for message in serialized_messages:
					file.write(message + '\n')
					number_of_written_messages += 1
		except IOError as e:
			self.logger.error("IOError occured while writing to file.")
			self.logger.error(str(e))
		except:
			self.logger.error("Error occured while writing to file.")

		self.logger.info("Written {0} messages to file.".format(number_of_written_messages))
