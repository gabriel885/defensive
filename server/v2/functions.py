import sys
import time

# NOTE - printed values will be returned. Don't user print() explicitly.
DEFAULT_REASON_EXCEPTION = "Error occurred"
FUNCTION_TIMEOUT = 5 # timeout in seconds
MAX_RETURN_OBJECT_SIZE = 30 # limit max response size in bytes


class TimeoutException(Exception): pass


class Decorators:
	
	@staticmethod
	def disclose_exception_decorator(func):
		def wrapp_function_with_exception(*args, **kwargs):
			try:
				res = func(*args, **kwargs)
				
				# don't allow to return None (XML-Server complains)
				if res is None:
					return DEFAULT_REASON_EXCEPTION
				
				# check result result type
				if type(res) is not int:
					return DEFAULT_REASON_EXCEPTION
				
				# check return result size
				if sys.getsizeof(res) > MAX_RETURN_OBJECT_SIZE:
					return DEFAULT_REASON_EXCEPTION
				
				return res
			except Exception as reason:
				return DEFAULT_REASON_EXCEPTION  # disclose reason to route
			pass
		
		return wrapp_function_with_exception
	
	@staticmethod
	def runtime_exception_decorator(func):
		import signal
		from contextlib import contextmanager
		
		
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
	print(funcs[sys.argv[1]](*sys.argv[2:]))
	
except TimeoutException as e:
	print(e)
	
except Exception as e:
	print(DEFAULT_REASON_EXCEPTION)
	#print(e)
