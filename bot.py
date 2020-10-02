from InstagramAPI import InstagramAPI
from time import time, sleep
from random import randint
import logging, threading, glob, os, sys, codecs, argsParser

class Bot(object):
	def __init__(self, username, password, img_folder, caption_file, posts_per_day, follows_per_day, keyword):
		format = "%(asctime)s: %(message)s"
		logging.basicConfig(format=format, level=logging.INFO, datefmt="[%D] %H:%M:%S")
		self.username = username
		self.password = password
		self.img_folder = img_folder
		self.caption_file = caption_file
		self.caption = self.initCaption()
		self.posts_per_day = posts_per_day if posts_per_day != None else 4
		self.time_between_posts = 24 * 3600 / self.posts_per_day
		self.follows_per_day = follows_per_day if posts_per_day != None else 100
		self.time_between_follows = 24 * 3600 / self.follows_per_day
		self.keyword = keyword if keyword != None else "picoftheday"
		self.bot = self.initBot()
		self.followers = []
		self.followings = []
		self.to_follow = []
		self.updateFollowers()
		self.updateFollowings()
		self.updateToFollow()

	@property
	def followers_nb(self):
		return len(self.followers)

	@property
	def followings_nb(self):
		return len(self.followings)

	@property
	def to_follow_nb(self):
		return len(self.to_follow)

	def initBot(self):
		bot = InstagramAPI(self.username, self.password)
		bot.login()

		return bot

	#TODO: manage multiple captions
	#maybe use json system with {photo:path, caption:"caption"}
	def initCaption(self):
		caption = ""
		
		try:
			with codecs.open(self.caption_file, "r", encoding = "utf8") as f:
				logging.info("Caption successfully loaded")
				caption = f.read()
		except Exception as e:
			logging.info("No caption file, caption will be blank")

		return caption


	def updateFollowers(self):
		self.followers = [str(user['pk']) for user in self.bot.getTotalSelfFollowers()]
		logging.info(f"Loaded {len(self.followers)} followers")

	def updateFollowings(self):
		self.followings = [str(user['pk']) for user in self.bot.getTotalSelfFollowings()]
		logging.info(f"Loaded {len(self.followings)} followings")

	def updateToFollow(self):
		#TODO: manage multiple keywords (pretty simple, just add for loop)
		if(self.bot.tagFeed(self.keyword)):
			items = self.bot.LastJson["ranked_items"]
			for item in items:
				if (self.bot.getMediaLikers(item["id"])):
					for liker in self.bot.LastJson["users"]:
						pk = str(liker["pk"])
						if (pk not in self.to_follow):
							self.to_follow.append(pk)
			logging.info(f"Loaded {len(self.to_follow)} persons to follow")
		else:
			logging.info(f"Failed to get persons to follow")
	
	def follow(self):
		while True:
			a = self.time_between_follows - 60 if (self.time_between_follows - 60) >= 0 else 0
			b = self.time_between_follows + 60
			sleep(randint(a, b))

			if (self.to_follow_nb == 0):
				self.updateToFollow()
			if (self.to_follow_nb == 0):
				logging.info("Nobody to follow")
			else:
				next_follow = self.to_follow.pop(0)
				self.bot.follow(next_follow)
				logging.info(f"Successfully followed {next_follow}")				

	def unfollow(self):
		while True:
			a = self.time_between_follows - 60 if (self.time_between_follows - 60) >= 0 else 0
			b = self.time_between_follows + 60
			sleep(randint(a, b))

			if (self.followings_nb == 0):
				self.updateFollowings()
			if (self.followings_nb == 0):
				logging.info("Nobody to unfollow")
			else:
				next_unfollow = self.followings.pop(0)
				self.bot.unfollow(next_unfollow)
				logging.info(f"Successfully unfollowed {next_unfollow}")
	
	def postPhoto(self):
		while true:
			a = self.time_between_posts - 1800 if (self.time_between_posts - 1800) >= 0 else 0
			b = self.time_between_posts + 1800
			sleep(randint(a, b))
			images_nb = 0

			try:
				images_nb = len(os.listdir(self.img_folder))
				logging(f"Found {images_nb} images to upload in {self.img_folder}/ folder")
			except expression as identifier:
				logging.info(f"No folder specified, not uploading any images")

			#TODO: add property to get next image to make code clearer
			if (images_nb == 0):
				#TODO: automatically download new images if no more
				logging.info(f"No more images to upload, please add some in the {self.img_folder} folder")
			else:
				image = os.listdir(self.img_folder)[0]
				self.bot.uploadPhoto(self.img_folder + "/" + image, self.caption)
				logging.info(f"Successfully uploaded {image}")
				os.remove(self.img_folder + "/" + image)

	def properties(self):
		return (f"username : {self.username}"
		f" password : {self.password}"
		f" img_folder : {self.img_folder}"
		f" caption_file : {self.caption_file}"
		f" caption : {self.caption}"
		f" posts_per_day : {self.posts_per_day}"
		f" follows_per_day : {self.follows_per_day}"
		f" keyword : {self.keyword}")

	def toString(self):
		return (f"{self.username} currently have "
		f"{self.followers_nb} followers, {self.followings_nb} followings, and "
		f"{self.to_follow_nb} persons to follow next")

	def info(self):
		while True:
			sleep(43200)
			logging.info(self.toString())

	def startBotting(self):
		logging.info("Starting the bot:\n" + self.toString())
		follow_thread = threading.Thread(target=self.follow).start()
		unfollow_thread = threading.Thread(target=self.unfollow).start()
		post_thread = threading.Thread(target=self.postPhoto).start()
		info_thread = threading.Thread(target=self.info).start()

#TODO:load config from file
if __name__ == "__main__":
	parser = argsParser.initParser()
	args = parser.parse_args()
	if ((args.username) and (args.password)):
		img_folder = args.image_folder if args.image_folder else None
		caption_file = args.caption_file if args.caption_file else None
		posts_per_day = args.posts_per_day if args.posts_per_day else None
		follows_per_day = args.follows_per_day if args.follows_per_day else None
		keyword = args.keyword if args.keyword else None
		bot = Bot(args.username, args.password, img_folder, caption_file,
		posts_per_day, follows_per_day, keyword)
		bot.startBotting()