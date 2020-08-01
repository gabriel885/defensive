from xmlrpc.server import SimpleXMLRPCServer

from container import docker_environment_decorator


class RemoteCodeExecutionThreadedServer(SimpleXMLRPCServer):
	EXECUTION_TIME = 5  # 45 seconds execution for each function
	
	def __init__(self, host, port, *args, **kwargs):
		SimpleXMLRPCServer.__init__(self, (host, port), *args, **kwargs)
		print("Starting v2 server on {}:{}".format(host, port))
	
	def run(self):
		""" run server"""
		self.serve_forever()


# function signature definitions (implementation are in functions.py file)


@docker_environment_decorator
def add(x, y) -> int:
	""" adding 2 numbers and returning sum"""
	pass


@docker_environment_decorator
def eval(expression):
	""" evaluating expressions """
	pass


@docker_environment_decorator
def divide(x, y) -> int:
	""" dividing x by y and return answer"""
	pass


@docker_environment_decorator
def multiply(x, y) -> int:
	""" multiply x by y and return answer """
	pass


@docker_environment_decorator
def sleep(n=0):
	""" sleep for n seconds (imitate busy computation) """
	pass


if __name__ == '__main__':
	HOST = "localhost"
	PORT = 8000
	
	server = RemoteCodeExecutionThreadedServer(HOST, PORT)
	
	# register functions
	server.register_function(add, "add")
	server.register_function(eval, "eval")
	server.register_function(divide, "divide")
	server.register_function(multiply, "multiply")
	
	server.register_function(sleep, "sleep")
	
	server.run()
	pass
