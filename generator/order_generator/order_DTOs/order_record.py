# class for representing order record object
class OrderRecord:
	def __init__(self):
		self.identifier = ""
		self.timestamp = 0
		self.direction = ""
		self.currency_pair = ""
		self.initial_px = 0
		self.fill_px = 0
		self.initial_volume = 0
		self.fill_volume = 0
		self.status = ""
		self.tag = ""
		self.description = ""
