from abc import ABCMeta, abstractmethod


# class for generating data
class Generator:
	__metaclass__ = ABCMeta

	# initialization function
	# set logger
	# set total number of generated values
	def __init__(self, logger):
		self.logger = logger
		self.total_number_of_generated_values = 0

	# data generation function
	# accepts amount of data instances to generate and metric instance
	# returns list of generated data
	@abstractmethod
	def generate(self, amount, metric):
		pass
