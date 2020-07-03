import tweepy
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import environ
import requests
import json

load_dotenv('.env')

def main(code):
	data = json.loads(requests.get("https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json").text)
	with open('test-json.json') as f:
  		data = json.load(f)

	data = data['utlas']

	place = [d for d in data if d['areaCode'] == code]

	recent_date = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d') # there is a one day delay on reporting
	today = [p for p in place if p['specimenDate'] == recent_date][0]

	old_result = place[7]

	daily_cases = [p['dailyLabConfirmedCases'] for p in place]
	
	days_nocases = 0
	for d in daily_cases:
		if d == 0:
			days_nocases += 1
		else:
			break

	print(days_nocases)
	print(daily_cases)

	## text variable
	day_inc = today['dailyLabConfirmedCases']
	total = today['totalLabConfirmedCases']
	date_f = datetime.strptime(recent_date, '%Y-%m-%d').strftime("%d %b")

	long_inc = today['totalLabConfirmedCases'] - old_result['totalLabConfirmedCases']
	old_date = datetime.strptime(old_result['specimenDate'], '%Y-%m-%d').strftime("%d %b")

	rate = today['dailyTotalLabConfirmedCasesRate']

	if(days_nocases >= 3):
		tweet = f"There have been {days_nocases} days since the last case of COVID-19 in Bristol. There have been {long_inc} cases since the {old_date}. There have been a total of {total} cases, at a rate of {rate} cases per 100k people."
	if(days_nocases < 3):
		tweet = f"There were {day_inc} cases of COVID-19 in Bristol on {date_f}, with {long_inc} cases since {old_date}. There have been a total of {total} cases, which is a rate of {rate} cases per 100k people."
		# tweet = f"There have been {total} COVID-19 cases in Bristol as of {date_f}. This is an increase of {day_inc} from {date_yf} and {week_inc} in the previous week."
	# send tweet
	return(tweet)



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

# # check authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Parameters
bristol_code = "E06000023"
output = main(bristol_code)
new_tweet = output

last_tweet = api.user_timeline(id = "@Bristol_C19", count = 1, tweet_mode='extended')[0]._json['full_text']

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
