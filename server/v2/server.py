import time
from xmlrpc.server import SimpleXMLRPCServer

from exception import disclose_exception_decorator, runtime_exception_decorator

from container import docker_environment_decorator



class RemoteCodeExecutionThreadedServer(SimpleXMLRPCServer):
	EXECUTION_TIME = 5  # 45 seconds execution for each function
	
	def __init__(self, host, port, *args, **kwargs):
		SimpleXMLRPCServer.__init__(self, (host, port), *args, **kwargs)
		print("Starting v2 server on {}:{}".format(host, port))
	
	def run(self):
		""" run server"""
		self.serve_forever()


@docker_environment_decorator
@disclose_exception_decorator
@runtime_exception_decorator
def add(x, y):
	if type(x) is not int and type(y) is not int:
		return 0
	print("inside add")
	return x + y


@docker_environment_decorator
@disclose_exception_decorator
@runtime_exception_decorator
def eval(expression):
	return eval(expression)


@docker_environment_decorator
@disclose_exception_decorator
@runtime_exception_decorator
def divide(x, y):
	if type(x) is not int and type(y) is not int:
		return 0
	if y == 0:
		# you can't divide in 0
		return 0 # confuse the user
	return x / y


@docker_environment_decorator
@disclose_exception_decorator
@runtime_exception_decorator
def multiply(x, y):
	if type(x) is not int and type(y) is not int:
		return 0
	return x * y


@docker_environment_decorator
@disclose_exception_decorator
@runtime_exception_decorator
def sleep(n=0):
	print("sleeping")
	time.sleep(n)
	print("finished sleeping")


if __name__ == '__main__':
	HOST = "localhost"
	PORT = 8000
	
	## TODO: MAKE SURE DOCKER IS RUNNING!!!
	
	server = RemoteCodeExecutionThreadedServer(HOST, PORT)
	
	
	# ### SAFE PICKLING only available during server startup ###
	#
	# from importlib import reload
	# import pickle
	# class DummyObject: pass
	#
	# # safely load files
	# functions = {
	# 	"add": open("functions/add", "wb").write(pickle.dumps(add)),
	# 	"divide": open("functions/divide", "wb").write(pickle.dumps(divide)),
	# 	"multiply": open("functions/multiply", "wb").write(pickle.dumps(multiply)),
	# 	"eval": open("functions/eval", "wb").write(pickle.dumps(eval)),
	# }
	#
	# # change file permissions to 400 (only read)
	# for f in functions.keys():
	# 	os.chmod("/functions/{}", 400)  # change permissions to 400
	#
	# pickle = DummyObject()
	# os = DummyObject()
	# sys = DummyObject()
	#
	# reload(pickle)
	# reload(os)
	# reload(sys)
	#
	# print ("pickle {}".format(pickle))
	# print ("os {}".format(os))
	# print ("sys {}".format(sys))
	
	# register loaded
	server.register_function(add, "add")
	server.register_function(eval, "eval")
	server.register_function(divide, "divide")
	server.register_function(multiply, "multiply")
	
	server.register_function(sleep, "sleep")
	
	server.run()
	pass
