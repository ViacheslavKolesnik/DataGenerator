from serializer.serializer import Serializer
from serializer.order_record.entity.order_record_pb2 import OrderRecord as ProtoOrderRecord
from serializer.order_record.entity.order_pb2 import Order as ProtoOrder
from generator.order.entities.order import Order
from generator.order.entities.order_record import OrderRecord
from config.config import Config


# class for serializing order records into strings
class OrderRecordSerializer(Serializer):
	# construct order records into strings
	# accepts list of order records
	# returns list of strings
	def serialize(self, order_record):
		proto_order = ProtoOrder()
		proto_order.identifier = order_record.order.identifier
		proto_order.direction = order_record.order.direction
		proto_order.currency_pair = order_record.order.currency_pair
		proto_order.initial_px = order_record.order.initial_px
		proto_order.fill_px = order_record.order.fill_px
		proto_order.initial_volume = order_record.order.initial_volume
		proto_order.fill_volume = order_record.order.fill_volume
		proto_order.tag = order_record.order.tag
		proto_order.description = order_record.order.description

		proto_order_record = ProtoOrderRecord()
		proto_order_record.status = order_record.status
		proto_order_record.timestamp = order_record.timestamp
		proto_order_record.order.CopyFrom(proto_order)

		serialized_order_record = proto_order_record.SerializeToString()

		return serialized_order_record

	def deserialize(self, string):
		proto_order_record = ProtoOrderRecord()
		proto_order_record.ParseFromString(string)

		order = Order()
		order.identifier = proto_order_record.order.identifier
		order.direction = proto_order_record.order.direction
		order.currency_pair = proto_order_record.order.currency_pair
		order.initial_px = round(proto_order_record.order.initial_px, Config.digit.px_digits)
		order.fill_px = round(proto_order_record.order.fill_px, Config.digit.px_digits)
		order.initial_volume = round(proto_order_record.order.initial_volume, Config.digit.volume_digits)
		order.fill_volume = round(proto_order_record.order.fill_volume, Config.digit.volume_digits)
		order.tag = proto_order_record.order.tag
		order.description = proto_order_record.order.description

		order_record = OrderRecord()
		order_record.order = order
		order_record.status = proto_order_record.status
		order_record.timestamp = proto_order_record.timestamp

		return order_record
