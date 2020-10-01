import sys, getopt

# username, password, img_folder, caption_file, posts_per_day, follows_per_day, keyword):

def main(argv):
	username = None
	password = None
	img_folder = "img"
	caption_file = None
	posts_per_day = 4
	follows_per_day = 150
	keyword = None
	
	try:
		opts, args = getopt.getopt(argv,"u:p:h")
	except getopt.GetoptError:
		print("error")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-u"):
			username = arg
		elif opt in ("-p"):
			password = arg
	print(username, password)

if __name__ == "__main__":
	main(sys.argv[1:])