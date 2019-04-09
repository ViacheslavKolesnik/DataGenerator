from generator.order.strategy.order_modify import OrderModifyStrategy


# order modify strategy for 'Partial filled' final status
class FinalStatusPartialFilled(OrderModifyStrategy):
	# modify order according to 'Partial filled' final status
	def modify(self, order, fill_px, fill_volume):
		order.fill_px = fill_px
		order.fill_volume = fill_volume
