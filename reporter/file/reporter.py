from reporter.reporter import Reporter


class FileReporter(Reporter):
	def __init__(self, writer_service):
		super(FileReporter, self).__init__()
		self.writer_service = writer_service

	def report(self, metric):
		report = super(FileReporter, self).report(metric)
		self.writer_service.write(report)
