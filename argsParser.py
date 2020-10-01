import argparse

#DOC
#https://stackabuse.com/command-line-arguments-in-python/
def initParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--password", help="set password")
	parser.add_argument("-u", "--username", help="set username")
	parser.add_argument("-p", "--password", help="set password")
	parser.add_argument("-p", "--password", help="set password")
	parser.add_argument("-p", "--password", help="set password")
	return parser