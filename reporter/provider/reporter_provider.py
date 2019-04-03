from config.config import Config
from config.constant.file import FILE_EXTENSION_REPORT, FILE_PERMISSION_REPORT
from config.constant.other import REPORT_OUTPUT_FILE, REPORT_OUTPUT_CONSOLE

from reporter.console.reporter import ConsoleReporter
from reporter.file.reporter import FileReporter
from service.file_service.writer.writer_file_service import FileWriter


class ReporterProvider:
	@staticmethod
	def get_reporter(report_output=REPORT_OUTPUT_CONSOLE, program_start_time=None, logger=None):
		if report_output == REPORT_OUTPUT_FILE:
			if program_start_time is not None and logger is not None:
				report_file = Config.file.report_file_path + program_start_time + FILE_EXTENSION_REPORT
				writer_service = FileWriter(logger, report_file, FILE_PERMISSION_REPORT)

				return FileReporter(writer_service)
			else:
				print("Error. Cannot instantiate FileLogger. No program_start_time specified. Using ConsoleLogger.")
				return ConsoleReporter()
		else:
			return ConsoleReporter()
