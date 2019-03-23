from configparser import ConfigParser

from constants.constants_config import DEFAULT_CONFIG_FILES
from constants.constants_datetime import MIN_START_DATE_TIMESTAMP, MAX_START_DATE_TIMESTAMP
from constants.constants_exit_codes import EXIT_CODE_FILE_ERROR, EXIT_CODE_CONFIG_READING_ERROR, EXIT_CODE_CONFIG_PARSING_ERROR, EXIT_CODE_CONFIG_PARSING_ERROR

from utils.utils import Utils
from config import Config
from config_parameters.currency_config import CurrencyConfig
from config_parameters.database_config import DataBaseConfig
from config_parameters.date_config import DateConfig
from config_parameters.description_config import DescriptionConfig
from config_parameters.digit_config import DigitConfig
from config_parameters.file_config import FileConfig
from config_parameters.log_config import LogConfig
from config_parameters.message_brocker_config import MessageBrokerConfig
from config_parameters.order_config import OrderConfig
from config_parameters.tag_config import TagConfig


# class for parsing and storing config parameters
# config_files - list of configuration files
class ConfigurationParser:
	config_files = None

	# initializing method
	# setting configuration files if passed else setting default configuration files
	def __init__(self, logger, config_files=None):
		self.logger = logger
		self.number_of_errors_in_configurations = 0
		if config_files is not None:
			self.config_files = config_files
			self.logger.info("Configuration files specified. Using user configurations.")
		else:
			self.config_files = DEFAULT_CONFIG_FILES
			self.logger.info("No configuration files specified. Using default configurations.")

	# reading config files into ConfigParser object
	# config_parser - ConfigParser object
	def __read_config_files(self, config_parser):
		try:
			config_parser.read(self.config_files)
			self.logger.info("Successfully read configuration files.")
		except IOError as e:
			self.logger.fatal("IOError occurred while reading config files:")
			self.logger.fatal(e)
			exit(EXIT_CODE_FILE_ERROR)
		except:
			self.logger.fatal("Error occurred while reading config files:")
			exit(EXIT_CODE_CONFIG_READING_ERROR)

	# parsing config
	# reading config files
	# parsing config files
	def parse_config(self):
		config_parser = ConfigParser()

		self.__read_config_files(config_parser)
		self.__parse_config_files(config_parser)

	# parsing config files
	# setting groups of parameters to proper field in Config
	def __parse_config_files(self, config_parser):
		Config.order = self.__parse_order_config(config_parser)
		Config.date = self.__parse_date_config(config_parser)
		Config.digit = self.__parse_digit_config(config_parser)
		Config.description = self.__parse_description_config(config_parser)
		Config.tag = self.__parse_tag_config(config_parser)
		Config.currency = self.__parse_currency_config(config_parser)
		Config.file = self.__parse_file_config(config_parser)
		Config.database = self.__parse_database_config(config_parser)
		Config.message_broker = self.__parse_message_broker_config(config_parser)
		Config.log = self.__parse_log_config(config_parser)

		if self.number_of_errors_in_configurations == 0:
			self.logger.info("Config parsing successful.")
		else:
			self.logger.fatal("Config parsing failed. Found {0} errors.".format(self.number_of_errors_in_configurations))
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

	# parsing order related parameters
	# return OrderConfig object
	def __parse_order_config(self, config_parser):
		order = None
		order_config = OrderConfig()

		try:
			order = config_parser['order']
		except:
			self.logger.fatal("Error while parsing order configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		if not order['number_of_orders_zone_red'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("NUMBER_OF_ORDERS_ZONE_RED must be not negative integer.")
		else:
			order_config.number_of_orders_zone_red = int(order['number_of_orders_zone_red'])

		if not order['number_of_orders_zone_green'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("NUMBER_OF_ORDERS_ZONE_GREEN must be not negative integer.")
		else:
			order_config.number_of_orders_zone_green = int(order['number_of_orders_zone_green'])

		if not order['number_of_orders_zone_blue'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("NUMBER_OF_ORDERS_ZONE_BLUE must be not negative integer.")
		else:
			order_config.number_of_orders_zone_blue = int(order['number_of_orders_zone_blue'])

		if not order['number_of_orders_total'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("NUMBER_OF_ORDERS_TOTAL must be positive integer.")
		else:
			order_config.number_of_orders_total = int(order['number_of_orders_total'])
		if self.number_of_errors_in_configurations == 0:
			total_number_of_orders = order_config.number_of_orders_zone_red + order_config.number_of_orders_zone_green + order_config.number_of_orders_zone_blue
			if total_number_of_orders != order_config.number_of_orders_total:
				self.number_of_errors_in_configurations += 1
				self.logger.error("NUMBER_OF_ORDERS_TOTAL must be equal to sum of NUMBER_OF_ORDERS_ZONE_RED, NUMBER_OF_ORDERS_ZONE_GREEN, NUMBER_OF_ORDERS_ZONE_BLUE.")
			if order_config.number_of_orders_total == 0:
				self.number_of_errors_in_configurations += 1
				self.logger.error("NUMBER_OF_ORDERS_TOTAL must be positive.")

		if not order['number_of_orders_per_chunk'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("NUMBER_OF_ORDERS_PER_CHUNK must be positive integer.")
		else:
			order_config.number_of_orders_per_chunk = int(order['number_of_orders_per_chunk'])
		if order_config.number_of_orders_per_chunk == 0:
			self.number_of_errors_in_configurations += 1
			self.logger.error("NUMBER_OF_ORDERS_PER_CHUNK must be positive integer.")

		return order_config

	# parsing date related parameters
	# return DateConfig object
	def __parse_date_config(self, config_parser):
		date = None
		date_config = DateConfig()

		try:
			date = config_parser['date']
		except:
			self.logger.fatal("Error while parsing date configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		if not date['dates_range_in_days'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("DATES_RANGE_IN_DAYS must be positive integer.")
		else:
			date_config.dates_range_in_days = int(date['dates_range_in_days'])
		if date_config.dates_range_in_days == 0:
			self.number_of_errors_in_configurations += 1
			self.logger.error("DATES_RANGE_IN_DAYS must be positive.")

		if not date['starting_date'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("STARTING_DATE must be a timestamp.")
		else:
			date_config.starting_date = int(date['starting_date'])
			if not MIN_START_DATE_TIMESTAMP < date_config.starting_date < MAX_START_DATE_TIMESTAMP:
				self.number_of_errors_in_configurations += 1
				self.logger.error("STARTING_DATE must be between {0} and {1}.".format(MIN_START_DATE_TIMESTAMP, MAX_START_DATE_TIMESTAMP))

		return date_config

	# parsing digit related parameters
	# return DigitConfig object
	def __parse_digit_config(self, config_parser):
		digit = None
		digit_config = DigitConfig()

		try:
			digit = config_parser['digit']
		except:
			self.logger.fatal("Error while parsing digit configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		if not digit['volume_digits'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("VOLUME_DIGITS must be not negative integer.")
		else:
			digit_config.volume_digits = int(digit['volume_digits'])

		if not digit['px_digits'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("PX_DIGITS must be not negative integer.")
		else:
			digit_config.px_digits = int(digit['px_digits'])

		return digit_config

	# parsing description related parameters
	# return DescriptionConfig object
	def __parse_description_config(self, config_parser):
		description = None
		description_config = DescriptionConfig()

		try:
			description = config_parser['description']
		except:
			self.logger.fatal("Error while parsing description configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		description_config.descriptions = Utils.get_list_from_string_with_coma_delimiter(description['descriptions'])

		if not description['descriptions_number'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("DESCRIPTIONS_NUMBER must be positive integer.")
		else:
			description_config.descriptions_number = int(description['descriptions_number'])
			if description_config.descriptions_number == 0:
				self.number_of_errors_in_configurations += 1
				self.logger.error("DESCRIPTIONS_NUMBER must be positive.")

		if not description_config.descriptions_number == len(description_config.descriptions):
			self.number_of_errors_in_configurations += 1
			self.logger.error("DESCRIPTIONS length must be equal to DESCRIPTIONS_NUMBER.")

		return description_config

	# parsing tag related parameters
	# return TagConfig object
	def __parse_tag_config(self, config_parser):
		tag = None
		tag_config = TagConfig()

		try:
			tag = config_parser['tag']
		except:
			self.logger.fatal("Error while parsing tag configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		self.number_of_errors_in_configurations= 0
		tag_config.tags = Utils.get_list_from_string_with_coma_delimiter(tag['tags'])

		if not tag['tags_number'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("TAGS_NUMBER must be positive integer.")
		else:
			tag_config.tags_number = int(tag['tags_number'])
			if tag_config.tags_number == 0:
				self.number_of_errors_in_configurations += 1
				self.logger.error("TAGS_NUMBER must be positive.")

		if not tag_config.tags_number == len(tag_config.tags):
			self.number_of_errors_in_configurations += 1
			self.logger.error("TAGS length must be equal to TAGS_NUMBER.")

		return tag_config

	# parsing currency related parameters
	# return CurrencyConfig object
	def __parse_currency_config(self, config_parser):
		currency = None
		currency_config = CurrencyConfig()

		try:
			currency = config_parser['currency']
		except:
			self.logger.fatal("Error while parsing currency configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		self.number_of_errors_in_configurations = 0
		currency_config.currency_pairs = Utils.get_list_from_string_with_coma_delimiter(currency['currency_pairs'])
		currency_config.currency_pair_values = Utils.get_list_from_string_with_coma_delimiter(currency['currency_pair_values'])

		if not currency['currency_value_pairs_number'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("CURRENCY_VALUE_PAIRS_NUMBER must be positive integer.")
		else:
			currency_config.currency_value_pairs_number = int(currency['currency_value_pairs_number'])
			if currency_config.currency_value_pairs_number == 0:
				self.number_of_errors_in_configurations += 1
				self.logger.error("CURRENCY_VALUE_PAIRS_NUMBER must be positive.")

		for iterator in range(len(currency_config.currency_pair_values)):
			try:
				currency_config.currency_pair_values[iterator] = float(currency_config.currency_pair_values[iterator])
			except ValueError:
				self.number_of_errors_in_configurations += 1
				self.logger.error("Values in CURRENCY_PAIR_VALUES must be float.")

		if not currency_config.currency_value_pairs_number == len(currency_config.currency_pairs) == len(currency_config.currency_pair_values):
			self.number_of_errors_in_configurations += 1
			self.logger.error("CURRENCY_PAIRS and CURRENCY_PAIR_VALUES lengths must be equal to CURRENCY_VALUE_PAIRS_NUMBER.")

		return currency_config

	# parsing file related parameters
	# return FileConfig object
	def __parse_file_config(self, config_parser):
		file = None
		file_config = FileConfig()

		try:
			file = config_parser['file']
		except:
			self.logger.fatal("Error while parsing file configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		file_config.data_output_file = file['data_output_file']
		file_config.report_file_path = file['report_file_path']

		return file_config

	# parsing database related parameters
	# return DataBaseConfig object
	def __parse_database_config(self, config_parser):
		database = None
		database_config = DataBaseConfig()

		try:
			database = config_parser['database']
		except:
			self.logger.fatal("Error while parsing database configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		database_config.user = database['user']
		database_config.password = database['password']
		database_config.host = database['host']
		database_config.database_name = database['database_name']
		if not database['port'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("Database PORT must be not negative integer.")
		else:
			database_config.port = int(database['port'])

		return database_config

	# parsing message broker parameters
	# return MessageBrokerConfig object
	def __parse_message_broker_config(self, config_parser):
		message_broker = None
		message_broker_config = MessageBrokerConfig()

		try:
			message_broker = config_parser['message_broker']
		except:
			self.logger.fatal("Error while parsing message broker configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		message_broker_config.user = message_broker['user']
		message_broker_config.password = message_broker['password']
		message_broker_config.host = message_broker['host']
		message_broker_config.virtual_host = message_broker['virtual_host']

		if not message_broker['port'].isdigit():
			self.number_of_errors_in_configurations += 1
			self.logger.error("Database PORT must be not negative integer.")
		else:
			message_broker_config.port = int(message_broker['port'])

		return message_broker_config

	# parsing log related parameters
	# return LogConfig object
	def __parse_log_config(self, config_parser):
		log = None
		log_config = LogConfig()

		try:
			log = config_parser['log']
		except:
			self.logger.fatal("Error while parsing log configuration file occurred. Missing configuration file.")
			exit(EXIT_CODE_CONFIG_PARSING_ERROR)

		log_config.info_enabled = log['log_info_enabled'] == 'True'
		log_config.error_enabled = log['log_error_enabled'] == 'True'

		return log_config
