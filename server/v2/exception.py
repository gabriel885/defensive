# import signal, sys
# from contextlib import contextmanager
#
#
# DEFAULT_REASON_EXCEPTION = "Error occurred"
# FUNCTION_TIMEOUT = 5 # timeout in seconds
# MAX_RETURN_OBJECT_SIZE = 30 # limit max response size in bytes
#
#
# class TimeoutException(Exception): pass
#
# @contextmanager
# def time_limit(seconds):
# 	def signal_handler(signum, frame):
# 		raise TimeoutException("Timed out!")
# 	signal.signal(signal.SIGALRM, signal_handler)
# 	signal.alarm(seconds)
# 	try:
# 		yield
# 	finally:
# 		signal.alarm(0)
#
#
# def runtime_exception_decorator(func):
# 	def wrap_function_with_timeout(*args, **kwargs):
# 		try:
# 			with time_limit(FUNCTION_TIMEOUT):
# 				return func(*args)
# 		except TimeoutException as e: # raise timeout exception
# 			print("Timed out!")
# 		pass
# 	return wrap_function_with_timeout
#
#
# def disclose_exception_decorator(func):
# 	def wrapp_function_with_exception(*args, **kwargs):
# 		try:
# 			res = func(*args, **kwargs)
#
# 			# don't allow to return None (XML-Server complains)
# 			if res is None:
# 				return DEFAULT_REASON_EXCEPTION
#
# 			# check result result type
# 			if type(res) is not int:
# 				return DEFAULT_REASON_EXCEPTION
#
# 			# check return result size
# 			if sys.getsizeof(res) > MAX_RETURN_OBJECT_SIZE:
# 				return DEFAULT_REASON_EXCEPTION
#
# 			return res
# 		except Exception as reason:
# 			print (reason) # print internally the reason
# 			return DEFAULT_REASON_EXCEPTION # disclose reason to route
# 		pass
#
# 	return wrapp_function_with_exception
#
#
