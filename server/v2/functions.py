import signal
import sys
import time
from contextlib import contextmanager

# NOTE - printed values will be returned. Don't user print() explicitly.

DEFAULT_REASON_EXCEPTION = "Error occurred"
FUNCTION_TIMEOUT = 5  # timeout in seconds
MAX_RETURN_OBJECT_SIZE = 30  # limit max response size in bytes


class TimeoutException(Exception):
	pass


class MemoryException(Exception):
	pass


class Decorators:
	@staticmethod
	def runtime_exception_decorator(func):
		@contextmanager
		def time_limit(seconds):
			def signal_handler(signum, frame):
				raise TimeoutException("Timed out! Max runtime is {} seconds".format(FUNCTION_TIMEOUT))
			
			signal.signal(signal.SIGALRM, signal_handler)
			signal.alarm(seconds)
			try:
				yield
			finally:
				signal.alarm(0)
		
		def wrap_function_with_timeout(*args, **kwargs):
			try:
				with time_limit(FUNCTION_TIMEOUT):
					return func(*args)
			except TimeoutException as e:  # raise timeout exception
				print(e)
			pass
		
		return wrap_function_with_timeout
	
	pass


@Decorators.runtime_exception_decorator
def add(x, y):
	x = int(x)
	y = int(y)
	return x + y


@Decorators.runtime_exception_decorator
def divide(x, y):
	y = int(y)
	x = int(x)
	if y == 0:
		# you can't divide in 0
		return 0  # confuse the user
	return x / y


@Decorators.runtime_exception_decorator
def multiply(x, y):
	x = int(x)
	y = int(y)
	return x * y


@Decorators.runtime_exception_decorator
def eval(expression):
	return eval(expression)


@Decorators.runtime_exception_decorator
def sleep(n=0):
	n = int(n)
	time.sleep(n)
	return "slept {} seconds".format(n)


funcs = {
	"add": add,
	"multiply": multiply,
	"divide": divide,
	"sleep": sleep,
	"eval": eval,
}

try:
	res = funcs[sys.argv[1]](*sys.argv[2:])
	if sys.getsizeof(res) > MAX_RETURN_OBJECT_SIZE:
		raise MemoryException("Memory response exceeded max allowed {} bytes".format(MAX_RETURN_OBJECT_SIZE))
	print(res)

except MemoryException as e:
	print(e)

except TimeoutException as e:
	print(e)

except Exception as e:
	print(DEFAULT_REASON_EXCEPTION)
