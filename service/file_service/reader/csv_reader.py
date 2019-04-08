import csv

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from service.file_service.file_service import FileService
from generator.order.entities.order_record import OrderRecord
from generator.order.entities.order import Order


# service for writing to file
class CSVFileReader(FileService):
	# initialization function
	# set logger, file string and file permission
	def __init__(self, logger, file_string, permission):
		super(CSVFileReader, self).__init__(logger, file_string, permission)

	# write messages to file
	# messages - list of messages
	# serializer - messages serializer
	# if serializer specified construct messages then write to file
	def read(self, seek_number):
		order_records = MemoryAllocationManager.get_list()

		try:
			with open(self.file_string, self.permission) as file:
				csv_reader = list(csv.reader(file))[seek_number:]
				for row in csv_reader:
					order = Order()
					order_record = OrderRecord()
					order_record.order = order

					order_record.order.identifier = row[0]
					order_record.order.direction = row[1]
					order_record.order.currency_pair = row[2]
					order_record.order.initial_px = row[3]
					order_record.order.fill_px = row[4]
					order_record.order.initial_volume = row[5]
					order_record.order.fill_volume = row[6]
					order_record.order.tag = row[7]
					order_record.order.description = row[8]
					order_record.status = row[9]
					order_record.timestamp = row[10]

					order_records.append(order_record)
		except IOError as e:
			self.logger.error("IOError occured while reading from file.")
			self.logger.error(e)
		except Exception as e:
			self.logger.error("Error occured while reading from file.")
			self.logger.error(e)

		return order_records
