from logger.file_logger.file_logger import FileLogger


# main program class
# handles program execution
class Launcher:
	# main initializing function of Data Generator
	# initialize logger
	def __init__(self):
		self.logger = FileLogger()
		self.logger.info("Logger initialized. Starting data generator.")

	# prepare to execute function
	def __prepare(self):
		pass

	# main execution function
	def __execute(self):
		pass

	# reporting function
	def __report(self):
		pass

	# main finish function
	def __finish(self):
		pass

	# main function of Data Generator
	# starting program execution
	# reporting program work
	# finishing program
	def launch(self):
		self.__execute()
		self.__report()
		self.__finish()


# Entry point to Data Generator
if __name__ == "__main__":
	launcher = Launcher()
	launcher.launch()
