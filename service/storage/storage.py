from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class Storage:
	def __init__(self):
		self.__store = MemoryAllocationManager.get_list()
		self.__put = 0
		self.__extracted = 0

	def put(self, item):
		self.__store.append(item)
		self.__put += 1

	def get(self, amount):
		return self.__store[:amount]

	def delete(self, amount):
		del self.__store[:amount]
		self.__extracted += amount

	def get_number_put(self):
		return self.__put

	def get_number_of_extracted(self):
		return self.__extracted

	def get_amount_stored(self):
		return len(self.__store)
