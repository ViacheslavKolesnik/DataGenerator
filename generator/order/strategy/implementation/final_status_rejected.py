from generator.order.strategy.order_modify import OrderModifyStrategy


# order modify strategy for 'Rejected' final status
class FinalStatusRejected(OrderModifyStrategy):
	# modify order according to 'Rejected' final status
	def modify(self, order, fill_px, fill_volume):
		order.fill_px = 0
		order.fill_volume = 0
