from abc import ABC, abstractmethod

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager


class GeneratorMetric(ABC):
	@abstractmethod
	def __init__(self):
		self._generation = MemoryAllocationManager.get_list()

	def get_generation(self):
		return self._generation
