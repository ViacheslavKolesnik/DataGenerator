from serializer.serializer import Serializer
from serializer.order_record.entity.order_record_pb2 import OrderRecord
from serializer.order_record.entity.order_pb2 import Order


# class for serializing order records into strings
class OrderRecordSerializer(Serializer):
	# construct order records into strings
	# accepts list of order records
	# returns list of strings
	def serialize(self, order_record):
		proto_order = Order()
		proto_order.identifier = order_record.order.identifier
		proto_order.direction = order_record.order.direction
		proto_order.currency_pair = order_record.order.currency_pair
		proto_order.initial_px = order_record.order.initial_px
		proto_order.fill_px = order_record.order.fill_px
		proto_order.initial_volume = order_record.order.initial_volume
		proto_order.fill_volume = order_record.order.fill_volume
		proto_order.tag = order_record.order.tag
		proto_order.description = order_record.order.description

		proto_order_record = OrderRecord()
		proto_order_record.status = order_record.status
		proto_order_record.timestamp = order_record.timestamp
		proto_order_record.order.CopyFrom(proto_order)

		serialized_order_record = str(proto_order_record.SerializeToString())

		return serialized_order_record
