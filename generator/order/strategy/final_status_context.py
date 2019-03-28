from config.constant.status import *

from generator.order.strategy.implementation.final_status_filled import FinalStatusFilled
from generator.order.strategy.implementation.final_status_partial_filled import FinalStatusPartialFilled
from generator.order.strategy.implementation.final_status_rejected import FinalStatusRejected


class FinalStatusContext:
	def get_strategy(self, final_status):
		if final_status == STATUS_FILLED:
			return FinalStatusFilled()
		elif final_status == STATUS_PARTIAL_FILLED:
			return FinalStatusPartialFilled()
		elif final_status == STATUS_REJECTED:
			return FinalStatusRejected()
