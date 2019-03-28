from config.constant.database import ORDER_RECORD_INSERT_PATTERN

from serializer.serializer import Serializer


# class for serializing order records into strings
class OrderRecordDataBaseSerializer(Serializer):

	# initialization function
	# set logger
	def __init__(self, logger):
		super(OrderRecordDataBaseSerializer, self).__init__(logger)

	# serialize order records into strings
	# accepts list of order records
	# returns list of strings
	def serialize(self, order_record):
		serialized_order_record = ORDER_RECORD_INSERT_PATTERN.format(
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

		return serialized_order_record
