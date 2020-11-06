import signal
from contextlib import contextmanager

from exceptions import TimeoutException


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException("Timed out! Max runtime is {} seconds".format(seconds))
	
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)
