from generator.order.strategy.order_modify import OrderModifyStrategy


class FinalStatusPartialFilled(OrderModifyStrategy):
	def modify(self, order, fill_px, fill_volume):
		order.fill_px = fill_px
		order.fill_volume = fill_volume
