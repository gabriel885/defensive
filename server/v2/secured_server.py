from base64 import b64decode
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from container import docker_environment_decorator

authorized_users = {
	'gabriel': 'P@ssW0rd'
}


class AuthRequestHandler(SimpleXMLRPCRequestHandler):
	
	def parse_request(self):
		if SimpleXMLRPCRequestHandler.parse_request(self):
			# next we authenticate
			if self.authenticate(self.headers):
				return True
			else:
				# if authentication fails, tell the client
				self.send_error(401, 'Authentication failed')
		return False
	
	@staticmethod
	def authenticate(headers):
		try:
			(basic, _, encoded) = headers.get('Authorization').partition(' ')
		except Exception as _:
			return False
		else:
			# Client authentication
			(basic, _, encoded) = headers.get('Authorization').partition(' ')
			assert basic == 'Basic', 'Only basic authentication supported'
			#    Encoded portion of the header is a string
			#    Need to convert to bytestring
			encoded_byte_string = encoded.encode()
			#    Decode Base64 byte String to a decoded Byte String
			decoded_bytes = b64decode(encoded_byte_string)
			#    Convert from byte string to a regular String
			decoded_string = decoded_bytes.decode()
			#   Get the username and password from the string
			(username, _, password) = decoded_string.partition(':')
			# check if authorized
			try:
				if authorized_users[username] == password:
					return True
				return False
			except Exception as _:
				return False
	
	pass


class RemoteCodeExecutionThreadedServer(SimpleXMLRPCServer):
	
	def __init__(self, host, port, *args, **kwargs):
		SimpleXMLRPCServer.__init__(self, (host, port), requestHandler=AuthRequestHandler, *args, **kwargs)
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
	
	server.register_introspection_functions()
	
	# register functions
	server.register_function(add, "add")
	server.register_function(eval, "eval")
	server.register_function(divide, "divide")
	server.register_function(multiply, "multiply")
	
	server.register_function(sleep, "sleep")
	
	server.run()
	pass
