from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class Storage:
	def __init__(self):
		self.__store = MemoryAllocationManager.get_list()
		self.__history = MemoryAllocationManager.get_list()
		self.__extracted = 0

	def put(self, item):
		if item not in self.__history:
			self.__store.append(item)
			self.__history.append(item)

	def get(self, amount):
		response = self.__store[:amount]
		return response

	def delete(self, items):
		for item in items:
			self.__store.remove(item)
			self.__extracted += 1

	def get_number_of_extracted(self):
		return self.__extracted

	def get_amount_stored(self):
		return len(self.__store)

	def get_history_size(self):
		return len(self.__history)
