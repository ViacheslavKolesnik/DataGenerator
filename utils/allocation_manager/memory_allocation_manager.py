import inspect

from config.constants.constants_exit_codes import EXIT_CODE_NOT_ENOUGH_MEMORY

from logger.logger import Logger

# class for memory-safe creation of data structures
class MemoryAllocationManager:
	# creates list
	# handles MemoryError while list creation
	@staticmethod
	def get_list():
		try:
			return list()
		except MemoryError:
			Logger.fatal("Function {0}: Error creating list. Not enough memory.".format(inspect.getouterframes(inspect.currentframe())[1].function))
			exit(EXIT_CODE_NOT_ENOUGH_MEMORY)

	# creates dictionary
	# handles MemoryError while dictionary creation
	@staticmethod
	def get_dict(argument):
		try:
			return dict(argument)
		except MemoryError:
			Logger.fatal("Function {0}: Error creating list. Not enough memory.".format(inspect.getouterframes(inspect.currentframe())[1].function))
			exit(EXIT_CODE_NOT_ENOUGH_MEMORY)
