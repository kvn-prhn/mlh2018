import praw
import config
import time
import os

comments_to_search = 5

DO_NOT_RESPOND = 0
TEST_COMMENT = 1

# Given comment text, can/should the bot reply to it?
def get_comment_response_code(comment):
	if "this is for testing" in comment.body:
		return TEST_COMMENT
	return DO_NOT_RESPOND

	
def generate_comment_reply(comment, responsecode):
	if responsecode == TEST_COMMENT:
		return "Test comment"
	return "Invalid Response Code"


	
def bot_login():
	print ("Logging in...")
	r = praw.Reddit('replybot', user_agent='TrumpReplyBot user agent')
	print ("Logged in!")

	return r

def run_bot(r, comments_replied_to):
	print ("Searching last " + str(comments_to_search) + " comments")

	for comment in r.subreddit('test').comments(limit=comments_to_search):
		comment_response_code = get_comment_response_code(comment)
		if not comment_response_code == DO_NOT_RESPOND and comment.id not in comments_replied_to and comment.author != r.user.me():
			resp = generate_comment_reply(comment, comment_response_code)
			comment.reply(resp)
			print ("Replied to comment " + comment.id)
			comments_replied_to.append(comment.id)
			with open ("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

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
	