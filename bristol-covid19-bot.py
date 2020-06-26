import tweepy
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import environ
import re

#dotenv.load_dotenv('.env')
load_dotenv('.env')

def main(code, api):
	d = pd.read_csv('covid-19-uk-data/data/covid-19-cases-uk.csv')
	d = d[d.AreaCode==code]
  
	## assuming cases always go up (i.e. recoveries aren't removed) the highest number
 	## will always be the most recent
	#cases = d['confirm']
	cases = d['TotalCases']

	date = datetime.strptime(d['Date'].iloc[-1], "%Y-%m-%d")
	date_f = date.strftime('%a %d %b')

	date_yesterday = date - timedelta(days=1)
	date_yf = date_yesterday.strftime('%a %d %b')

	date_lastweek = date - timedelta(days=7)
	date_lwf = date_lastweek.strftime('%a %d %b')

	TC = []
	for c in cases:
		if c == "1 to 4":
		  TC.append(2)
		else:
		  TC.append(int(c))

	cases = TC
	d['TC'] = TC

	# total cases
	total = cases[-1]

	# days of no cases
	nocases = d[d.TotalCases == total]
	date_nocases = datetime.strptime(nocases['Date'].iloc[0], "%Y-%m-%d")
	days_nocases = (date - date_nocases).days

	# previous tweets
	lastten_tweets = api.user_timeline(id = "@Bristol_C19", count = 10)
	# print(lastten_tweets[0].text)
	for tweet in lastten_tweets:
		prev_dates = re.search('There are [0-9]{3,} COVID-19 cases in Bristol as of ([A-Z]{1}[a-z]{2} [0-9]{2} [A-Z]{1}[a-z]{2})', tweet.text)
		if(prev_dates is not None):			
			if(prev_dates.group(1) == date_lwf):
				week_count = re.search('There are ([0-9]{3,})', tweet.text).group(1) 
			if(prev_dates.group(1) == date_yf):
				last_tweet = tweet.text
  
	# previous day
	yesterday_count = re.search('There are ([0-9]{3,})', last_tweet).group(1)
	day_inc = total - int(yesterday_count)
	


	week_inc = total - int(week_count)

	if(days_nocases >= 3):
		tweet = f"There have been {days_nocases} days since the last case of COVID-19 in Bristol. There has been {week_inc} cases in the previous week."
	if(days_nocases < 3):
		tweet = f"There are {total} COVID-19 cases in Bristol as of {date_f}. This is an increase of {day_inc} from {date_yf} and {week_inc} in the previous week."
	# print(tweet)
	# send tweet
	return([tweet, last_tweet])



# API login
# Authenticate to Twitter
one = environ.get('ONE')
two = environ.get('TWO')
three = environ.get('THREE')
four = environ.get('FOUR')

auth = tweepy.OAuthHandler(one, two)
auth.set_access_token(three,four)

# # Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

# check authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Parameters
bristol_code = "E06000023"
output = main(bristol_code, api)
new_tweet = output[0]
last_tweet = output[1]

if new_tweet != last_tweet:
	print("#-- Old tweet --#")
	print(last_tweet)
	print("#-- New tweet --#")
	print(new_tweet)
	txt = input("Shall we tweet?\n")
	if txt == "y":
		api.update_status(new_tweet)
	else:
		print("# -- Not tweeted -- #")
else: 
 	print("#-- No updates --#")
