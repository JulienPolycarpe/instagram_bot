from InstagramAPI import InstagramAPI
from time import time

class Bot(object):
	def __init__(self, username, password, img_folder, caption_file, posts_per_day, follows_per_day, keyword):
		self.username = username
		self.password = password
		self.img_folder = img_folder
		self.caption_file = caption_file
		self.posts_per_day = posts_per_day
		self.time_between_posts = 24 * 3600 / posts_per_day
		self.follows_per_day = follows_per_day
		self.time_between_follows = 24 * 3600 / follows_per_day
		self.start_time = time()
		self.keyword = keyword
		self.bot = self.initBot()
		self.followers = []
		self.followings = []
		self.to_follow = []
		self.updateFollowers()
		self.updateFollowings()
		self.updateToFollow()

	def initBot(self):
		followers = []
		to_follow = []

		bot = InstagramAPI(self.username, self.password)
		bot.login()

		return bot

	def updateFollowers(self):
		self.followers = [str(user['pk']) for user in self.bot.getTotalSelfFollowers()]

	def updateFollowings(self):
		self.followings = [str(user['pk']) for user in self.bot.getTotalSelfFollowings()]

	def updateToFollow(self):
		if(self.bot.tagFeed(self.keyword)):
			items = self.bot.LastJson["ranked_items"]
			for item in items:
				if (self.bot.getMediaLikers(item["id"])):
					for liker in self.bot.LastJson["users"]:
						pk = str(liker["pk"])
						if (pk not in self.to_follow):
							self.to_follow.append(pk)

test = Bot("streetartforeveryone",
			"THEBIBILLOU033//",
			"images",
			"caption.txt",
			4,
			150,
			"streertart")
print(len(test.followers), len(test.followings), len(test.to_follow))