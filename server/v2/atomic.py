import threading


class AtomicCounter:
	"""An atomic, thread-safe incrementing counter with automatic decrementation after timout """
	
	def __init__(self, max_increment=5):
		"""Initialize a new atomic counter to given initial value (default 0)."""
		self.value = 0
		self.max_increment = max_increment
		self._lock = threading.Lock()
	
	def increment(self):
		"""Atomically increment the counter by num (default 1) and return the
		new value.
		"""
		if self.value >= self.max_increment:
			return False
		
		with self._lock:  # blocking operation
			self.value += 1
			return True
	
	def decrement(self):
		
		if self.value <= 0:
			return
		
		with self._lock:
			self.value -= 1
		return
	
	def get(self):
		return self.value
