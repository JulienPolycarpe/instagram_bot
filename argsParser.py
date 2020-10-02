import argparse

#DOC
#https://stackabuse.com/command-line-arguments-in-python/
def initParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--password", help="set password")
	parser.add_argument("-u", "--username", help="set username")
	parser.add_argument("-f", "--image-folder", help="set image folder")
	parser.add_argument("-c", "--caption-file", help="set caption file")
	parser.add_argument("-ppd", "--posts-per-day", help="set posts per day number")
	parser.add_argument("-fpd", "--follows-per-day", help="set follows per day number")
	parser.add_argument("-k", "--keyword", help="set keyword to find persons to follow")
	return parser