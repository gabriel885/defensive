from xmlrpc.server import SimpleXMLRPCServer
from math import * ## don't remove, this is used by eval()

class XMLRPCServer(SimpleXMLRPCServer):
	
	def __init__(self, host, port, *args, **kwargs):
		SimpleXMLRPCServer.__init__(self, (host, port), *args, **kwargs)
		print("Starting v1 server on {}:{}".format(host, port))
	
	def run(self):
		""" run server"""
		self.serve_forever()
	
	def _dispatch(self, method, params):
		try:
			# We are forcing the 'export_' prefix on methods that are
			# callable through XML-RPC to prevent potential security
			# problems
			func = getattr(self, 'expose_' + method)
		except AttributeError:
			raise Exception("method {} is not supported".format(method))
		else:
			return func(*params)
	
	def expose_add(self, x, y):
		return x + y
	
	def expose_eval(self, expression):
		return eval(expression)
	
	def expose_divide(self, x, y):
		return x / y
	
	def expose_multiply(self, x, y):
		return x * y


if __name__ == '__main__':
	HOST = "localhost"
	PORT = 8000
	
	server = XMLRPCServer(HOST, PORT)
	server.run()
	pass
