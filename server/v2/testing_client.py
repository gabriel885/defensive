import xmlrpc.client

if __name__ == "__main__":
	HOST = "localhost"
	PORT = 8000
	
	USERNAME = 'gabriel'
	PASSWORD = 'P@ssW0rd'
	
	proxy = xmlrpc.client.ServerProxy("http://{}:{}@{}:{}/".format(USERNAME, PASSWORD, HOST, PORT), allow_none=True)
	
	print("Calling add(4,2) method on server. Result {}".format(proxy.add(4, 2)))
	
	print("Calling multiply(42,21) method on server. Result {}".format(proxy.multiply(42, 21)))
	
	print("Calling divide(64,8) method on server. Result {}".format(proxy.divide(64, 8)))
