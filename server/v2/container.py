from os import chmod, getcwd, path

import docker

import consts
from atomic import AtomicCounter

container_counter = AtomicCounter(consts.MAX_NUM_CONTAINERS)  # count how many containers are currently running
chmod(consts.FUNCTIONS_FILE, 0o400)  # set functions.py file with read-only permission

client = docker.from_env()  # instantiate docker client instance


def docker_environment_decorator(func):  # receive function and function arguments to run inside a container
	def wrapped_with_decorator(*args):
		# command to execute inside the container
		run_pycode = 'python {} {} {}'.format(
			consts.FUNCTIONS_FILE, func.__name__, " ".join([str(arg) for arg in args]))
		
		if not container_counter.increment():  # check if another container can be ran
			return "Cannot execute code, max number of resources exceeded. Try again later..."
		
		# execute command inside a container. Bind with read-only mode function.py file
		# running container is synchronous until the result is received from the container as stdout
		result = client.containers.run(
			image=consts.PYTHON_DOCKER_IMAGE,  # image of the container
			command=run_pycode,  # command to run inside the container
			privileged=False,  # user running command inside the container is not privileged
			auto_remove=True,  # remove container after running is completed
			mem_limit=consts.CONTAINER_MEMORY_LIMIT,
			network_disabled=True,  # disable container network
			# grant read only permissions for binded functions.py file!
			volumes={'{}/{}'.format(getcwd(), consts.FUNCTIONS_FILE): {
				'bind': path.join(consts.ROOT_DIR, consts.FUNCTIONS_FILE), 'mode': 'ro'},
				'{}/{}'.format(getcwd(), consts.CONSTS_FILE): {
					'bind': path.join(consts.ROOT_DIR, consts.CONSTS_FILE), 'mode': 'ro'}}
		).decode('utf-8').strip()  # decode stdout
		
		container_counter.decrement()  # decrement total number of running containers
		
		print("result from container: '{}'".format(result))
		
		return result
	
	return wrapped_with_decorator
