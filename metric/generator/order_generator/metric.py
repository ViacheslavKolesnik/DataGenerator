from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from metric.generator.metric import GeneratorMetric


class OrderGeneratorMetric(GeneratorMetric):
	def __init__(self):
		super(OrderGeneratorMetric, self).__init__()
		self._red_zone_order_generation = MemoryAllocationManager.get_list()
		self._green_zone_order_generation = MemoryAllocationManager.get_list()
		self._blue_zone_order_generation = MemoryAllocationManager.get_list()
		self._file_insertion = MemoryAllocationManager.get_list()
		self._message_broker_publishing = MemoryAllocationManager.get_list()
		self._file_reading = MemoryAllocationManager.get_list()
		self._database_writing = MemoryAllocationManager.get_list()

	def get_red_zone_order_generation(self):
		return self._red_zone_order_generation

	def get_green_zone_order_generation(self):
		return self._green_zone_order_generation

	def get_blue_zone_order_generation(self):
		return self._blue_zone_order_generation

	def get_file_insertion(self):
		return self._file_insertion

	def get_message_broker_publishing(self):
		return self._message_broker_publishing

	def get_file_reading_and_parsing(self):
		return self._file_reading

	def get_database_writing(self):
		return self._database_writing
