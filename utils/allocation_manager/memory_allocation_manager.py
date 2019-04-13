import inspect

from config.constant.exit_code import EXIT_CODE_NOT_ENOUGH_MEMORY

from logger.logger import Logger

# class for memory-safe creation of data structures
class MemoryAllocationManager:
	logger = None

	# initialization function
	@classmethod
	def initialize(cls, logger):
		cls.logger = logger

	# creates list
	# handles MemoryError while list creation
	@classmethod
	def get_list(cls):
		try:
			return list()
		except MemoryError:
			cls.logger.fatal("Function {0}: Error creating list. Not enough memory.".format(inspect.getouterframes(inspect.currentframe())[1].function))
			exit(EXIT_CODE_NOT_ENOUGH_MEMORY)

	# creates dictionary
	# handles MemoryError while dictionary creation
	@classmethod
	def get_dict(cls):
		try:
			return dict()
		except MemoryError:
			cls.logger.fatal("Function {0}: Error creating list. Not enough memory.".format(inspect.getouterframes(inspect.currentframe())[1].function))
			exit(EXIT_CODE_NOT_ENOUGH_MEMORY)
