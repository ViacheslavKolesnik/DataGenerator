from config.constant.other import ORDER_RECORD_STRING_DELIMETER

from generator.order.entities.order import Order
from generator.order.entities.order_record import OrderRecord


class OrderRecordFromString:
	@staticmethod
	def get_order_record(string):
		order = Order()
		order_record = OrderRecord()
		order_record.order = order

		string_items = string.split(ORDER_RECORD_STRING_DELIMETER)
		iterator = 0

		for attr, value in order_record.__dict__.items():
			if value == order:
				for attr1, value1 in value.__dict__.items():
					setattr(value, attr1, string_items[iterator])
					iterator += 1
			else:
				setattr(order_record, attr, string_items[iterator])
				iterator += 1

		return order_record
