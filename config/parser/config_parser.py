from abc import ABC, abstractmethod


# class for parsing and storing config parameters
# config_file - list of configuration files
class ConfigurationParser(ABC):
	# initializing method
	# setting configuration files if passed else setting default configuration files
	@abstractmethod
	def __init__(self, logger, config_files):
		self.logger = logger
		self.number_of_errors_in_configurations = 0
		self.config_files = config_files

	# parse config
	@abstractmethod
	def parse_config(self):
		pass
