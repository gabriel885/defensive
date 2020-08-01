import sys
import time

# NOTE - printed values will be returned. Don't user print() explicitly.

def add(x, y):
	x = int(x)
	y = int(y)
	return x + y


def divide(x, y):
	y = int(y)
	x = int(x)
	if y == 0:
		# you can't divide in 0
		return 0  # confuse the user
	return x / y


def multiply(x, y):
	x = int(x)
	y = int(y)
	return x * y


def eval(expression):
	return eval(expression)


def sleep(n=0):
	n = int(n)
	time.sleep(n)
	return "slept {} seconds".format(n)

funcs = {
	"add": add,
	"multiply": multiply,
	"divide": divide,
	"sleep": sleep,
	"eval": eval,
}


try:
	print(funcs[sys.argv[1]](*sys.argv[2:]))
except Exception as e:
	#print (e)
	print("Error occurred")
