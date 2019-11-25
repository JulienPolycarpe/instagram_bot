from InstagramAPI import InstagramAPI
from PIL import Image
from random import randint
import glob, os, configparser, time, logging, sys


def init():
	logging.basicConfig(filename = LOG_FILE, level=logging.INFO)
	ig_bot = InstagramAPI(USERNAME, PASSWORD)
	ig_bot.login()
	return ig_bot


def addFuturFollowings():
	ig_bot.tagFeed(HASHTAG)

	l = []
	n = 0
	items = ig_bot.LastJson["ranked_items"]

	for photo in items: 
		ig_bot.getMediaLikers(photo["id"])
		for userLiker in ig_bot.LastJson["users"]:
			l.append(str(userLiker["pk"])) #username for the username (pk is user id)
			n += 1
	logging.info(str(time.ctime()) + ' : succesfully added ' + str(n) + ' ids to follow')

	return l


def addFuturUnfollowings():
	l = []
	for user in ig_bot.getTotalSelfFollowings():
		l.append(str(user['pk']))
	logging.info(str(time.ctime()) + ' : succesfully added ' + str(len(ig_bot.getTotalSelfFollowings())) + ' ids to unfollow')
	return l


def postNextPhoto():

	#if upload folder is empty
	if( len(os.listdir(PHOTO_PATH)) ) == 0:
		print(str(time.ctime()) + ' : no more photos to upload, stopping the bot')
		#TODO : automatically download new photos from google
		sys.exit()
	else:
		#posting photos
		photo = os.listdir(PHOTO_PATH)[0]
		ig_bot.uploadPhoto(PHOTO_PATH +"/" + photo, CAPTION)
		logging.info(str(time.ctime()) + " : successfully uploaded ", photo, "next post in ", DELAY_BETWEEN_POSTS, " seconds")
		os.remove(PHOTO_PATH + "/" + photo)


def bot():
	ids_to_unfollow = addFuturUnfollowings()
	ids_to_follow = addFuturFollowings()
	posting_time = int(time.time())

	#the more followings you have, the less time the bot will wait to unfollow them
	#if you have 500 followings, it will unfollow the 500 first before unfollowing
	#the last person you followed(1 follow every 3 minutes, then 1 unfollow every 3 minutes)
	#250 followings -> 25h before unfollow
	while 1:
		
		if(int(time.time()) - DELAY_BETWEEN_POSTS >= posting_time ):
			posting_time = int(time.time())
			postNextPhoto()

		if(len(ids_to_follow) == 0):
			ids_to_follow = addFuturFollowings() #refresh the line when finished following it

		next_follow = ids_to_follow.pop(0)
		next_unfollow = ids_to_unfollow.pop(0)

		ig_bot.follow(next_follow)
		ids_to_unfollow.append(next_follow)
		n = randint(190, 200)
		logging.info( str(time.ctime()) + " : succesfully followed " + next_follow + ", now waiting " + str(n) + " seconds before unfollowing someone" )
		time.sleep(n)
		ig_bot.unfollow(next_unfollow)
		n = randint(190, 200)
		logging.info( str(time.ctime()) + " : succesfully unfollowed " + next_unfollow + ", now waiting " + str(n) + " seconds before following someone" )
		time.sleep(n)



if __name__ == '__main__':

	config = configparser.ConfigParser()
	config.read('config.ini')

	LOG_FILE = config['DEFAULT']['log_file']
	USERNAME = config['DEFAULT']['username']
	PASSWORD = config['DEFAULT']['password']
	PHOTO_PATH = config['DEFAULT']['photo_path']
	CAPTION = config['DEFAULT']['caption']
	DELAY_BETWEEN_POSTS = int(config['DEFAULT']['delay_between_posts'])
	HASHTAG = config['DEFAULT']['hashtag_to_follow']

	ig_bot = init()
	bot()