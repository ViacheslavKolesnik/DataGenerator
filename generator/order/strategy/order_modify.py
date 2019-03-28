from abc import ABCMeta, abstractmethod


class OrderModifyStrategy:
	__metaclass__ = ABCMeta

	@abstractmethod
	def modify(self, order, fill_px, fill_volume):
		pass
