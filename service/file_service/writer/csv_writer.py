import os
import csv

from service.file_service.file_service import FileService


# service for writing data to csv file
class CSVFileWriter(FileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		directory = os.path.dirname(file_string)
		os.makedirs(directory, exist_ok=True)

		super(CSVFileWriter, self).__init__(logger, file_string, permission)

	# write message to file
	def write(self, order_record):
		try:
			with open(self.file_string, self.permission) as file:
				order_record_writer = csv.writer(file)
				order_record_writer.writerow([
					order_record.order.identifier,
					order_record.order.direction,
					order_record.order.currency_pair,
					order_record.order.initial_px,
					order_record.order.fill_px,
					order_record.order.initial_volume,
					order_record.order.fill_volume,
					order_record.order.tag,
					order_record.order.description,
					order_record.status,
					order_record.timestamp
				])
		except IOError as e:
			self.logger.error("IOError occured while writing to file.")
			self.logger.error(str(e))
		except:
			self.logger.error("Error occured while writing to file.")
