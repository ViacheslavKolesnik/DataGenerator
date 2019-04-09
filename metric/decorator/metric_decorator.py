import time

from config.constant.other import SECOND_TO_MICROSECOND_CONVERTING_COEF


# annotation to count function execution time
def timeit(method):
	# metrics - list used to append calculated metrics
	# counts function execution time using processor dependent time
	def timed(*args, metrics):
		start_time = time.perf_counter()
		result = method(*args)
		end_time = time.perf_counter()

		execution_time = int((end_time - start_time) * SECOND_TO_MICROSECOND_CONVERTING_COEF)

		if execution_time != 0:
			metrics.append(int((end_time - start_time) * SECOND_TO_MICROSECOND_CONVERTING_COEF))

		return result

	return timed
