from config.constant.other import ORDER_RECORD_STRING_DELIMETER


class OrderRecord:
	def __init__(self):
		self.order = None
		self.status = ""
		self.timestamp = 0

	def __repr__(self):
		return "{0}{1}{2}{3}{4}".format(
			self.order,
			ORDER_RECORD_STRING_DELIMETER,
			self.status,
			ORDER_RECORD_STRING_DELIMETER,
			self.timestamp
		)
