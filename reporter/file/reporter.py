from reporter.reporter import Reporter


# class for reporting to file
class FileReporter(Reporter):
	def __init__(self, writer_service):
		super(FileReporter, self).__init__()
		self.writer_service = writer_service

	# metric - OrderGeneratorMetric to be used in report
	def report(self, metric):
		report = super(FileReporter, self).report(metric)
		self.writer_service.write(report)
