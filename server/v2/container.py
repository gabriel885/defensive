# CREATING A CONTAINER SHOULD BE AN ATOMIC OPERATION

from os import chmod, getcwd

import docker
from atomic import AtomicCounter

# Docker container configurations
PYTHON_DOCKER_IMAGE = "python:3"
CONTAINER_MEMORY_LIMIT = '4m'  # 4 megabytes

MAX_NUM_CONTAINERS = 3
container_counter = AtomicCounter(MAX_NUM_CONTAINERS)

FUNCTIONS_FILE = "functions.py"
# read-only
chmod(FUNCTIONS_FILE, 0o400)

client = docker.from_env()


def docker_environment_decorator(func):
	def wrapped_with_decorator(*args):
		run_pycode = 'python {} {} {}'.format(FUNCTIONS_FILE, func.__name__, " ".join([str(arg) for arg in args]))
		
		if not container_counter.increment():
			return "Cannot execute code, max number of resources exceeded. Try again later..."
		
		result = client.containers.run(
			image=PYTHON_DOCKER_IMAGE,
			command=run_pycode,
			privileged=False,
			auto_remove=True,
			mem_limit=CONTAINER_MEMORY_LIMIT,
			network_disabled=True,
			# read only permission!
			volumes={'{}/{}'.format(getcwd(), FUNCTIONS_FILE): {'bind': '/functions.py', 'mode': 'ro'}}
		).decode('ascii').strip()
		
		container_counter.decrement()
		
		print("result from container: '{}'".format(result))
		
		return result
	
	return wrapped_with_decorator
