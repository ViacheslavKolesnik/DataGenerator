from order_status import OrderStatus
from order_status_timestamp import OrderStatusTimeStamp
from datetime import datetime


class Order:
	def __init__(self):
		self.identifier = ""
		self.timestamp = None
		self.direction = ""
		self.currency_pair = ""
		self.initial_px = 0
		self.fill_px = 0
		self.initial_volume = 0
		self.fill_volume = 0
		self.status = None
		self.tag = ""
		self.description = ""
