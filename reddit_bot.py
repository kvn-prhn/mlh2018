import praw
import config
import time
import os
import requests
import sys
import string
import random

sentiment_api_url = "https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"

reply_to_comments = False
include_sentiments = True
comments_to_search = 20

# comment response codes
DO_NOT_RESPOND = 0
TEST_COMMENT = 1
GLOBAL_WARMING = 2
KANYE_KARDASHIAN = 3
RUSSIA = 4
PUTIN = 5
DIET_COKE = 6
TRUMP_INSULT = 7
NEW_YORK = 8
tweetimpeach = "As has been stated by numerous legal scholars, I have the absolute right to PARDON myself,
but why would I do that when I have done nothing wrong? In the meantime, the never ending Witch Hunt, 
led by 13 very Angry and Conflicted Democrats (& others) continues into the mid-terms!"
tweetimpeach2="are you allowed to impeach a president for gross incompetence?"
tweetimpeach3="We need a President who isn't a laughing stock to the entire World. We need a truly great leader, a genius at strategy and winning. Respect!"
fkface="Amazing how the haters & losers keep tweeting the name “F**kface Von Clownstick” like they are so original & like no one else is doing it…"
twitter = "Thanks- many are saying I'm the best 140 character writer in the world. It's easy when it's fun."
econ= "Employment is up, Taxes are DOWN. Enjoy!"
COFEVE = 12
THE_WALL = 13
MAC_MILLER = 14
THE_DONALD = 15
CHINA = 16
MAGMA = 17
WINDMILLS = 18
KATE_MIDDLETON = 19


# Given the comment, sentiment, and response code, generate a response
# comment class: https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
# sentiment: number between 0 (negative) and 1 (positive). -1 for when there is no sentiment analysis
# response code: See the list of codes above
def generate_comment_reply(comment, sentiment):
	print(comment.body)
	print(sentiment)
	print("+++\n")
	lowerc = comment.body.lower()
	if "global warming" in lowerc:
		if "china" in lowerc:
                    return "The concept of global warming was created by and for the Chinese in order to make U.S. manufacturing non-competitive. \n\nhttps://twitter.com/realDonaldTrump/status/265895292191248385"
		return "It’s freezing and snowing in New York--we need global warming! \n\nhttps://twitter.com/realdonaldtrump/status/266259787405225984?lang=en"
	if "diet coke" in lowerc or "diet soda" in lowerc:
		return "I have never seen a thin person drinking Diet Coke.\n\nhttps://twitter.com/realDonaldTrump/status/257552283850653696https://twitter.com/realDonaldTrump/status/257552283850653696"
        if "trump" in lowerc and "impeach" in lowerc:
            xra=random.random(1,3)
            if xra is 1:
                return tweetimpeach
            elif xra is 2:
                return tweetimpeach2
            else:
                return tweetimpeach3 
        if "trump" in lowerc and "fuckface" in lowerc:
            return fkface
        if "trump" in lowerc and "twitter" in lowerc:
            return twitter
        if "trump" in lowerc:
            if "economy" in lowerc or "taxes" in lowerc:
                return econ

	return ""

	
	
def bot_login():
	print ("Logging in...")
	r = praw.Reddit('replybot', user_agent='TrumpReplyBot user agent')
	print ("Logged in!")

	return r

def run_bot(r, comments_replied_to):
	print ("Searching last " + str(comments_to_search) + " comments")
	all_comments = []
	for comment in r.subreddit('politics').comments(limit=comments_to_search):
		all_comments.append(comment)
	comment_sentiments = []
	for comment in all_comments:
		comment_sentiments.append(-1) # -1 when it is not being used.
	
	if include_sentiments:
		sentiment_docs = []
		i = 0
		for comment in all_comments:
			sentiment_docs.append({'id': str(i), 'language': 'en', 'text': str(comment.body)});
			i = i + 1
		print(sentiment_docs)
		documents = {'documents' : sentiment_docs}
		headers = {'Ocp-Apim-Subscription-Key': config.subscription_key, 'Content-Type': "application/json"}
		# sentiment API stuff
		response = requests.post(sentiment_api_url, headers=headers, json=documents)
		sentiments = response.json()
		for sres in sentiments['documents']:
			comment_sentiments.insert(int(sres['id']), sres['score'])
	
	i = 0
	print(all_comments)
	for comment in all_comments:
		if comment.id not in comments_replied_to and comment.author != r.user.me():
			resp = generate_comment_reply(comment, comment_sentiments[i])
			if reply_to_comments and not len(resp) > 0:
				comment.reply(resp)
				print ("Replied to comment " + comment.id)
			print ("Response: " + str(resp))
			
			if reply_to_comments:
				comments_replied_to.append(comment.id)
				with open ("comments_replied_to.txt", "a") as f:
					f.write(comment.id + "\n")
		i = i + 1
	
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
	
