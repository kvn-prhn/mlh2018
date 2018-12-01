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
GLOBAL_WARMING_1 = "The concept of global warming was created by and for the Chinese in order to make U.S. manufacturing non-competitive. \n\nhttps://twitter.com/realDonaldTrump/status/265895292191248385"
GLOBAL_WARMING_2 = "It’s freezing and snowing in New York--we need global warming! \n\nhttps://twitter.com/realdonaldtrump/status/266259787405225984?lang=en"
GLOBAL_WARMING_3 = "Windmills are the greatest threat in the US to both bald and golden eagles. Media claims fictional 'global warming’ is worse.\n\nhttps://twitter.com/realDonaldTrump/status/509436043368873984"
KANYE_KARDASHIAN = "Thank you Kanye, very cool! \n\nhttps://twitter.com/realDonaldTrump/status/989225812166696960"
RUSSIA = 4
PUTIN = 5
DIET_COKE = "I have never seen a thin person drinking Diet Coke.\n\nhttps://twitter.com/realDonaldTrump/status/257552283850653696https://twitter.com/realDonaldTrump/status/257552283850653696"
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
TAXES_ECONOMY = "Employment is up, Taxes are DOWN. Enjoy! \n\nhttps://twitter.com/realDonaldTrump/status/986218862625648640"
COFEVE = 12
THE_WALL = "We have to maintain strong borders or we will no longer have a country that we can be proud of – and if we show any weakness, millions of people will journey into our country. \n\nhttps://twitter.com/realDonaldTrump/status/1009928980475138048"
MAC_MILLER = "It was just announced that @MacMiller’s song 'DonaldTrump' went platinum—tell  Mac Miller to kiss my ass!\n\nhttps://twitter.com/realDonaldTrump/status/309346134600601601"
THE_DONALD_1 = ""
CHINA = "The concept of global warming was created by and for the Chinese in order to make U.S. manufacturing non-competitive.\nhttps://twitter.com/realDonaldTrump/status/265895292191248385"
MAGA = "My supporters are the smartest, strongest, most hard working and most loyal that we have seen in our countries history. It is a beautiful thing to watch as we win elections and gather support from all over the country. As we get stronger, so does our country. Best numbers ever!\nhttps://twitter.com/realDonaldTrump/status/1007974129474121728"
WINDMILLS = "Windmills are the greatest threat in the US to both bald and golden eagles. Media claims fictional ‘global warming’ is worse.\nhttps://twitter.com/realDonaldTrump/status/509436043368873984"
KATE_MIDDLETON = "Who wouldn't take Kate's [Middleston] picture and make lots of money if she does the nude sunbathing thing. Come on Kate!\nhttps://twitter.com/realDonaldTrump/status/247757867032117248"
MAKING_DEALS = "Deals are my art form. Other people paint beautifully or write poetry. I like making deals, preferably big deals. That's how I get my kicks \n\nhttps://twitter.com/realdonaldtrump/status/549590421190770688?lang=en"
WITCH_HUNT_1 = "A total WITCH HUNT with massive conflicts of interest! \n\nhttps://twitter.com/realDonaldTrump/status/975720503997620224"
WITCH_HUNT_2 = "A TOTAL WITCH HUNT!!! \n\nhttps://twitter.com/realDonaldTrump/status/983662953894436864"

# Given the comment, sentiment, and response code, generate a response
# comment class: https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
# sentiment: number between 0 (negative) and 1 (positive). -1 for when there is no sentiment analysis
# response code: See the list of codes above
def generate_comment_reply(comment, sentiment):
	print(comment.body)
	print(sentiment)
	print("+++\n")
	lowerc = comment.body.lower()
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
	if "global warming" in lowerc:
		if "china" in lowerc or "chinese" in lowerc:
			return GLOBAL_WARMING_1
		# else
		if random.random() < 0.5:
			return GLOBAL_WARMING_2
		else:
			return GLOBAL_WARMING_3
	if "diet coke" in lowerc or "diet soda" in lowerc:
		return DIET_COKE
	
	if "trump" in lowerc and sentiment < 0.9 and sentiment > 0.2:
		return "Every time I speak of the haters and losers I do so with great love and affection. They cannot help the fact that they were born fucked up!\n https://twitter.com/realDonaldTrump/status/516382177798680576"
	if "trump" in lowerc and sentiment < 0.2:
		return "SEE YOU IN COURT, THE SECURITY OF OUR NATION IS AT STAKE!\n https://twitter.com/realdonaldtrump/status/829836231802515457?lang=en"
	if "new york" in lowerc:
		return "It’s freezing and snowing in New York--we need global warming!\n https://twitter.com/realdonaldtrump/status/266259787405225984?lang=en"

	if "trump" in lowerc and ("economy" in lowerc or "taxes" in lowerc or "employment" in lowerc):
		return TAXES_ECONOMY
	if ("kanye" in lowerc or "kardashian" in lowerc) and sentiment > 0.5:
		return KANYE_KARDASHIAN
	if "deal" in lowerc and ("trump" in lowerc or "donald" in lowerc):
		return MAKING_DEALS
	if ("trump" in lowerc or "president" in lowerc) and ("russia" in lowerc or "investigation" in lowerc):
		if random.random() < 0.5:
			return WITCH_HUNT_1
		else:
			return WITCH_HUNT_2
	if "china" in lowerc or "chinese" in lowerc:
		return CHINA
	if "maga" in lowerc or "make america great again" in lowerc:
		return MAGA
	if "windmills" in lowerc:
		return WINDMILLS
	if "kate middleton" in lowerc:
		return KATE_MIDDLETON
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
		documents = {'documents' : sentiment_docs}
		headers = {'Ocp-Apim-Subscription-Key': config.subscription_key, 'Content-Type': "application/json"}
		# sentiment API stuff
		response = requests.post(sentiment_api_url, headers=headers, json=documents)
		sentiments = response.json()
		for sres in sentiments['documents']:
			comment_sentiments.insert(int(sres['id']), sres['score'])
	
	i = 0
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
	
