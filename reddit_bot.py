import praw
import config
import time
import os

comments_to_search = 1

# Given comment text, can/should the bot reply to it?
def can_reply_to_comment(text):
	
	return True
	
def process_reply(text):
	return "test"

def bot_login():
	print ("Logging in...")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "The Reddit Commenter v1.0")
	print ("Logged in!")

	return r

def run_bot(r, comments_replied_to):
	print ("Searching last " + comments_to_search + " comments")

	for comment in r.subreddit('test').comments(limit=comments_to_search):
		if can_reply_to_comment(comment.body) and comment.id not in comments_replied_to and comment.author != r.user.me():
			print ("String with \"sample user comment\" found in comment " + comment.id)
			print (comment)
			print(type(comment))
			#comment.reply("Hey, I like your comment!")
			#print "Replied to comment " + comment.id

			#comments_replied_to.append(comment.id)

			#with open ("comments_replied_to.txt", "a") as f:
			#	f.write(comment.id + "\n")

	print ("Search Completed.")

	print (comments_replied_to)

	print ("Sleeping for 10 seconds...")
	#Sleep for 10 seconds...		
	time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print (comments_replied_to)

while True:
	run_bot(r, comments_replied_to)
	