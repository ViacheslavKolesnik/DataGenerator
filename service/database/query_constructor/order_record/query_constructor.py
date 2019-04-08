from config.constant.database import ORDER_RECORD_INSERT_PATTERN

from service.database.query_constructor.query_constructor import DBQueryConstructor


# class for serializing order records into strings
class OrderRecordDBQueryConstructor(DBQueryConstructor):
	def __init__(self):
		self.counter = 0

	# construct order records into strings
	# accepts list of order records
	# returns list of strings
	def construct(self, order_record):
		order_record_db_query = ORDER_RECORD_INSERT_PATTERN.format(
			self.counter,
			order_record.order.identifier,
			order_record.order.currency_pair,
			order_record.order.direction,
			order_record.status,
			order_record.timestamp,
			order_record.order.initial_px,
			order_record.order.fill_px,
			order_record.order.initial_volume,
			order_record.order.fill_volume,
			order_record.order.description,
			order_record.order.tag
		)
		self.counter += 1

		return order_record_db_query
