from generator.order.strategy.order_modify import OrderModifyStrategy


class FinalStatusRejected(OrderModifyStrategy):
	def modify(self, order, fill_px, fill_volume):
		order.fill_px = 0
		order.fill_volume = 0
