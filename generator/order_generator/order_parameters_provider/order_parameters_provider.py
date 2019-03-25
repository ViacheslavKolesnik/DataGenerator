from __future__ import division

from datetime import datetime
from math import sin, cos, tan, ceil

from utils.allocation_manager.memory_allocation_manager import MemoryAllocationManager
from utils.utils import Utils
from config.config import Config
from config.constants.constants_datetime import *
from config.constants.constants_linear_congruent import *
from config.constants.constants_identifier import *
from config.constants.constants_direction import *
from config.constants.constants_status import *
from config.constants.constants_currency import *
from config.constants.constants_other import SECOND_TO_MICROSECOND_CONVERTING_COEF


# class responsible for order parameters generating
class OrderParametersProvider:
	# initialization function
	# set initial linear congruent number
	# set list of dates in specified range from specified starting date
	# linear_congruent_number - number used for generating order parameters
	def __init__(self, initial_congruent_number, start_date):
		self.linear_congruent_number = self.__generate_linear_congruent_number(initial_congruent_number)

		self.order_dates_in_range = MemoryAllocationManager.get_list()
		for iterator in range(Config.date.dates_range_in_days):
			order_date = start_date + ONE_UNIX_TIMESTAMP_DAY * iterator
			if datetime.fromtimestamp(order_date / SECOND_TO_MICROSECOND_CONVERTING_COEF).weekday() < WEEKEND_START_NUMBER:
				self.order_dates_in_range.append(order_date)

	# update linear congruent number
	def update_provider(self):
		self.linear_congruent_number = self.__generate_linear_congruent_number(self.linear_congruent_number)

	# generate next linear congruent number using previous
	def __generate_linear_congruent_number(self, congruent_number):
		congruent_number = Utils.modulo((LIN_CON_COEF_A * congruent_number + LIN_CON_COEF_C), LIN_CON_COEF_M)
		return congruent_number

	# generate order identifier
	def generate_identifier(self):
		sin_parameter = sin(self.linear_congruent_number) * ID_FUNCTION_MULTIPLIER_COEF
		tan_parameter = abs(tan(sin_parameter)) * ID_FUNCTION_MULTIPLIER_COEF
		identifier_first_part = int(abs(cos(sin_parameter)) * ID_PART_MULTIPLIER_COEF + tan_parameter)
		identifier_second_part = int(abs(cos(tan_parameter)) * ID_PART_MULTIPLIER_COEF + sin_parameter)
		identifier = str(identifier_first_part).zfill(ID_PART_LENGTH) + str(identifier_second_part).zfill(ID_PART_LENGTH)

		return identifier

	# generate list of dates for order
	# count - number of dates to generate
	def generate_dates(self, count):
		dates = MemoryAllocationManager.get_list()
		congruent_number = self.linear_congruent_number

		for iterator in range(count):
			time_value = Utils.modulo(congruent_number, ONE_UNIX_TIMESTAMP_DAY - 1)
			date_identifier = Utils.modulo(abs(int(ceil(sin(congruent_number)))), len(self.order_dates_in_range))
			date_value = self.order_dates_in_range[date_identifier]
			datetime_value = date_value + time_value

			dates.append(datetime_value)
			congruent_number = self.__generate_linear_congruent_number(congruent_number)

		dates.sort()

		return dates

	# generate order direction
	def generate_direction(self):
		direction_identifier = Utils.modulo(abs(int(ceil(sin(self.linear_congruent_number)))), DIRECTIONS_NUMBER)
		direction = DIRECTIONS[direction_identifier]

		return direction

	# generate order tag
	def generate_tag(self):
		tag_identifier = Utils.modulo(self.linear_congruent_number, Config.tag.tags_number)
		tag = Config.tag.tags[tag_identifier]

		return tag

	# generate order description
	def generate_description(self):
		description_identifier = Utils.modulo(self.linear_congruent_number, Config.description.descriptions_number)
		description = Config.description.descriptions[description_identifier]

		return description

	# generate order final status
	def generate_final_status(self):
		final_status_identifier = Utils.modulo(self.linear_congruent_number, FINAL_STATUSES_NUMBER)
		final_status = FINAL_STATUSES[final_status_identifier]

		return final_status

	# generate order currency pair
	def generate_currency_pair(self):
		currency_pair_identifier = Utils.modulo(self.linear_congruent_number, Config.currency.currency_value_pairs_number)
		currency_pair = Config.currency.currency_pairs[currency_pair_identifier]

		return currency_pair

	# generate order initial px
	def generate_initial_px(self):
		initial_px_identifier = Utils.modulo(self.linear_congruent_number, Config.currency.currency_value_pairs_number)
		initial_px = Config.currency.currency_pair_values[initial_px_identifier]

		return initial_px

	# generate order fill px depending on initial px
	def generate_fill_px(self, initial_px):
		fill_px_max_deviation = initial_px / DIFFERENCE_PERCENTAGE_DELIMITER
		fill_px_deviation = Utils.modulo(CURRENCIES_RAND_COEF, fill_px_max_deviation * PX_DIFFERENCE_MULTIPLIER)
		fill_px = initial_px + fill_px_max_deviation - fill_px_deviation

		return fill_px

	# generate order initial volume
	def generate_initial_volume(self):
		initial_volume = Utils.modulo(self.linear_congruent_number, INITIAL_VOLUME_MAX_NUMBER) + INITIAL_VOLUME_MIN_NUMBER

		return initial_volume

	# generate order fill volume depending on initial volume
	def generate_fill_volume(self, initial_volume):
		fill_volume_max_deviation = initial_volume / DIFFERENCE_PERCENTAGE_DELIMITER
		fill_volume_deviation = Utils.modulo(CURRENCIES_RAND_COEF, fill_volume_max_deviation)
		fill_volume = initial_volume - fill_volume_deviation

		return fill_volume
