from instagramAPI import InstagramAPI

class bot(object):
	def __init__(self, username, password, img_folder, caption_file, post_delay, follow_delay):
		self.username = username
		self.password = password
		self.img_folder = img_folder
		self.caption_file = caption_file
		self.post_delay = post_delay
		self.follow_delay = follow_delay

	def connect(self):
		pass