import time

from config.constant.other import SECOND_TO_MICROSECOND_CONVERTING_COEF


def timeit(method):
	def timed(*args, metrics):
		start_time = time.time()
		result = method(*args)
		end_time = time.time()

		execution_time = int((end_time - start_time) * SECOND_TO_MICROSECOND_CONVERTING_COEF)

		if execution_time != 0:
			metrics.append(int((end_time - start_time) * SECOND_TO_MICROSECOND_CONVERTING_COEF))

		return result

	return timed
