# CREATING A CONTAINER SHOULD BE AN ATOMIC OPERATION

import docker
from exception import runtime_exception_decorator
from atomic import AtomicCounter
from os import getcwd

# Docker container configurations
PYTHON_DOCKER_IMAGE = "python:3"
# PYTHON_DOCKER_IMAGE = "python:3.7-alpine"
CONTAINER_MEMORY_LIMIT = '4m'  # 4 megabytes

MAX_NUM_CONTAINERS = 3
container_counter = AtomicCounter(MAX_NUM_CONTAINERS)

FUNCTIONS_FILE = "functions.py"

client = docker.from_env()


def docker_environment_decorator(func):
	
	#@runtime_exception_decorator
	def wrapped_with_decorator(*args):
		
		#serialized = yaml.dump({'py_code': func(*args)})
		
		# import yaml
		#run_pycode = 'python -c """print({})""" '.format(func(*args))
		
		#serialized = json.dumps(func(*args))
		
		# import inspect
		# print(inspect.getsource(func))
		#
		# run_pycode = 'python -c """print({})""" '.format(func(*args))
		#
		
		print ("host {} {} {}".format(FUNCTIONS_FILE, func.__name__, " ".join([str(arg) for arg in args])))
		
		run_pycode = 'python {} {} {}'.format(FUNCTIONS_FILE, func.__name__, " ".join([str(arg) for arg in args]))
		
		#install_pip = "python -m pip install yaml"
		
		if not container_counter.increment():
			return "Cannot execute code, max number of resources exceeded. Try again later..."
		
		print("running container to execute code...")
		
		# container = client.containers.create(image=PYTHON_DOCKER_IMAGE)
		# container.start()
		# exit_code, result = container.exec_run(cmd="echo hello world")
		# result = result.decode("utf-8")
		#
		# container.kill()
		# print("result from container.exec_run {}".format(exit_code, result))
		# container_counter.decrement()
		#
		# return {"result": result, "exit_code": exit_code}
		
		result = client.containers.run(
			image=PYTHON_DOCKER_IMAGE,
			command=run_pycode,
			privileged=False,
			auto_remove=True,
			mem_limit=CONTAINER_MEMORY_LIMIT,
			network_disabled=True,
			# read only permission!
			volumes={'{}/{}'.format(getcwd(),FUNCTIONS_FILE): {'bind': '/functions.py', 'mode': 'ro'}}
		).decode('ascii')
		
		print("result from container.exec_run {}'".format(result))
		container_counter.decrement()
	
		return {"result": result}
	
	return wrapped_with_decorator

# return wrapped_with_docker_client

# def docker_wrapped_func(*args):
#     run_pycode = "python -c '''print ('hello from container')''' "
#
#     if not container_counter.increment():
#         return "Cannot execute code, max number of resources exceeded. Try again later..."
#
#     client = docker.from_env()
#     print("Docker Info".format(client.info()))
#
#     print("running container to execute code...")
#
#     container = client.containers.create(image=PYTHON_DOCKER_IMAGE)
#     container.start()
#     exit_code, result = container.exec_run(cmd=run_pycode)
#     result = result.decode("utf-8")
#
#     container.kill()
#     print("result from container.exec_run {} {}".format(exit_code, result))
#     container_counter.decrement()
#
#     return {"result": result, "exit_code": exit_code}
#
#     # result = client.containers.run(
#     #     image=PYTHON_DOCKER_IMAGE,
#     #     command=run_pycode,
#     #     privileged=False,
#     #     auto_remove=True,
#     #     mem_limit=CONTAINER_MEMORY_LIMIT,  # 4MB
#     #     network_disabled=True
#     # )
#     # result = result.decode("utf-8")
#     # container_counter.decrement()
#     # print("result: {}".format(result))
#     # return result.strip()
#
# return docker_wrapped_func
#

# inject pip libraries to docker machine
# def docker_environment_decorator(func):
#     def docker_wrapped_func(*args):
#         run_pycode = "python -c '''print ('hello from container')''' "
#
#         if not container_counter.increment():
#             return "Cannot execute code, max number of resources exceeded. Try again later..."
#
#         client = docker.from_env()
#         print("running container to execute code...")
#
#         container = client.containers.create(image=PYTHON_DOCKER_IMAGE)
#         container.start()
#         exit_code, result = container.exec_run(cmd=run_pycode)
#         result = result.decode("utf-8")
#
#         container.kill()
#         print("result from container.exec_run {} {}".format(exit_code, result))
#         container_counter.decrement()
#
#         return {"result": result, "exit_code": exit_code}
#
#         # result = client.containers.run(
#         #     image=PYTHON_DOCKER_IMAGE,
#         #     command=run_pycode,
#         #     privileged=False,
#         #     auto_remove=True,
#         #     mem_limit=CONTAINER_MEMORY_LIMIT,  # 4MB
#         #     network_disabled=True
#         # )
#         # result = result.decode("utf-8")
#         # container_counter.decrement()
#         # print("result: {}".format(result))
#         # return result.strip()
#
#     return docker_wrapped_func
