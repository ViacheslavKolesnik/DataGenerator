import os

from service.file_service.file_service import FileService


# service for writing to file
class FileWriter(FileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		directory = os.path.dirname(file_string)
		os.makedirs(directory, exist_ok=True)

		super(FileWriter, self).__init__(logger, file_string, permission)

	# write message to file
	def write(self, message):
		try:
			with open(self.file_string, self.permission) as file:
				file.write(message + '\n')
		except IOError as e:
			self.logger.error("IOError occured while writing to file.")
			self.logger.error(str(e))
		except:
			self.logger.error("Error occured while writing to file.")
