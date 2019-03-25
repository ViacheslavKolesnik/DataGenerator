import inspect

from config.constants.constants_exit_codes import EXIT_CODE_DIVISION_BY_ZERO

from logger.logger import Logger


# class with helpful functions
class Utils:
	logger = None

	# initialization function
	@classmethod
	def initialize(cls, logger):
		cls.logger = logger

	# divides two numbers
	# handles ZeroDivisionError while division
	# returns result of the division
	@classmethod
	def divide(cls, dividend, divider):
		if divider == 0:
			cls.logger.fatal("Function {0}: Division by zero.".format(inspect.getouterframes(inspect.currentframe())[1].function))
			exit(EXIT_CODE_DIVISION_BY_ZERO)
		else:
			return dividend / divider

	# modulo operation for two numbers
	# handles ZeroDivisionError while modulo
	# returns result of the modulo operation
	@classmethod
	def modulo(cls, dividend, divider):
		if divider == 0:
			cls.logger.fatal("Function {0}: Division by zero.".format(inspect.getouterframes(inspect.currentframe())[1].function))
			exit(EXIT_CODE_DIVISION_BY_ZERO)
		else:
			return dividend % divider

	# splits string by coma delimiter
	# returns list
	@staticmethod
	def get_list_from_string_with_coma_delimiter(string):
		return string.split(',')
