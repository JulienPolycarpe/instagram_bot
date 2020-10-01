from InstagramAPI import InstagramAPI
from time import time, sleep
import logging
import threading

class Bot(object):
	def __init__(self, username, password, img_folder, caption_file, posts_per_day, follows_per_day, keyword):
		format = "%(asctime)s: %(message)s"
		logging.basicConfig(format=format, level=logging.INFO, datefmt="[%D] %H:%M:%S")
		self.username = username
		self.password = password
		self.img_folder = img_folder
		self.caption_file = caption_file
		self.posts_per_day = posts_per_day
		self.time_between_posts = 24 * 3600 / posts_per_day
		self.follows_per_day = follows_per_day
		self.time_between_follows = 24 * 3600 / follows_per_day
		self.keyword = keyword
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
		followers = []
		to_follow = []

		bot = InstagramAPI(self.username, self.password)
		bot.login()

		return bot

	def updateFollowers(self):
		self.followers = [str(user['pk']) for user in self.bot.getTotalSelfFollowers()]
		logging.info(f"Loaded {len(self.followers)} followers")

	def updateFollowings(self):
		self.followings = [str(user['pk']) for user in self.bot.getTotalSelfFollowings()]
		logging.info(f"Loaded {len(self.followings)} followings")

	def updateToFollow(self):
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
			sleep(self.time_between_follows)
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
			sleep(self.time_between_follows)
			if (self.followings_nb == 0):
				self.updateFollowings()
			if (self.followings_nb == 0):
				logging.info("Nobody to unfollow")
			else:
				next_unfollow = self.followings.pop(0)
				self.bot.unfollow(next_unfollow)
				logging.info(f"Successfully unfollowed {next_unfollow}")
	
	def toString(self):
		return (f"{self.username} currently have "
		f"{self.followers_nb} followers, {self.followings_nb} followings, and "
		f"{self.to_follow_nb} persons to follow next")

	def info(self):
		while True:
			sleep(600)
			logging.info(self.toString())

	def startBotting(self):
		logging.info("Starting the bot:\n" + self.toString())
		follow_thread = threading.Thread(target=self.follow).start()
		unfollow_thread = threading.Thread(target=self.unfollow).start()
		info_thread = threading.Thread(target=self.info).start()

			

		
test = Bot("streetartforeveryone",
			"THEBIBILLOU033//",
			"images",
			"caption.txt",
			4,
			150,
			"streetart")
test.startBotting()