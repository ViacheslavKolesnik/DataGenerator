from abc import ABC, abstractmethod


class DBQueryConstructor(ABC):
	@abstractmethod
	def construct(self, *args):
		pass
