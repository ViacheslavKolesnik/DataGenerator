from generator.order.strategy.order_modify import OrderModifyStrategy


# order modify strategy for 'Filled' final status
class FinalStatusFilled(OrderModifyStrategy):
	# modify order according to 'Filled' final status
	def modify(self, order, fill_px, fill_volume):
		order.fill_px = fill_px
		order.fill_volume = order.initial_volume
