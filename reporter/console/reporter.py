from reporter.reporter import Reporter


# class for reporting to console
class ConsoleReporter(Reporter):
	def __init__(self):
		super(ConsoleReporter, self).__init__()

	# metric - OrderGeneratorMetric to be used in report
	def report(self, metric):
		report = super(ConsoleReporter, self).report(metric)
		print(report)
