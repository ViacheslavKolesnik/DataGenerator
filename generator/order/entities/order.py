from config.constant.other import ORDER_RECORD_STRING_DELIMETER


class Order:
	def __init__(self):
		self.identifier = ""
		self.direction = ""
		self.currency_pair = ""
		self.initial_px = 0.0
		self.fill_px = 0.0
		self.initial_volume = 0.0
		self.fill_volume = 0.0
		self.tag = ""
		self.description = ""

	def __repr__(self):
		return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}".format(
			self.identifier,
			ORDER_RECORD_STRING_DELIMETER,
			self.direction,
			ORDER_RECORD_STRING_DELIMETER,
			self.currency_pair,
			ORDER_RECORD_STRING_DELIMETER,
			self.initial_px,
			ORDER_RECORD_STRING_DELIMETER,
			self.fill_px,
			ORDER_RECORD_STRING_DELIMETER,
			self.initial_volume,
			ORDER_RECORD_STRING_DELIMETER,
			self.fill_volume,
			ORDER_RECORD_STRING_DELIMETER,
			self.tag,
			ORDER_RECORD_STRING_DELIMETER,
			self.description
		)
