import inspect
from statistics import mean

from config.constant.exit_code import EXIT_CODE_DIVISION_BY_ZERO, EXIT_CODE_NUMBER_EXPECTED

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

	# accepts list of numbers
	# returns maximum value in list
	@staticmethod
	def get_max(values):
		return max(values)

	# accepts list of numbers
	# returns minimum value in list
	@staticmethod
	def get_min(values):
		return min(values)

	# accepts list of numbers
	# returns rounded mean of all values in list
	@classmethod
	def get_mean(cls, values):
		for value in values:
			cls.__check_if_integer_or_float(value)

		return round(mean(values))

	# accepts list of numbers
	# returns rounded sum of all values in list
	@classmethod
	def get_sum(cls, values):
		for value in values:
			cls.__check_if_integer_or_float(value)

		return round(sum(values))

	# accepts value
	# passes if given value is integer or float
	# if fails exits from program
	@classmethod
	def __check_if_integer_or_float(cls, value):
		if not isinstance(value, int) and not isinstance(value, float):
			cls.logger.fatal("Cannot get mean from given list. Values in list should be integers or floats.")
			exit(EXIT_CODE_NUMBER_EXPECTED)
