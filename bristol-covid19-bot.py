import tweepy
import pandas as pd
from datetime import datetime, timedelta
import dotenv
import os

dotenv.load_dotenv('.env')

def main(code):
  d = pd.read_csv('Daily_COVID-19/Data/cases_by_utla.csv')
  d = d[d.GSS_CD==code]
  
  ## assuming cases always go up (i.e. recoveries aren't removed) the highest number
  ## will always be the most recent
  cases = d['confirm']
  
  # total cases
  total_index = cases.idxmax()
  total = d['confirm'][total_index]
  
  # previous day
  day_inc = total - cases.values[-2]

  # previous week
  week_inc = total - cases.values[-7]
  
  # date of most recent data
  date = datetime.strptime(d['date'][total_index], "%d/%m/%Y")
  date_f = date.strftime('%a %d %b')
  # previous date
  prev_date = date - timedelta(days=1)
  prev_date = prev_date.strftime('%a %d %b')

  tweet = f"There are {total} COVID-19 cases in Bristol as of {date_f}. This is an increase of {day_inc} from {prev_date} and {week_inc} in the previous week."
  #print(tweet)
  # send tweet
  return(tweet)


# Authenticate to Twitter
one = os.environ.get('ONE')
two = os.environ.get('TWO')
three = os.environ.get('THREE')
four = os.environ.get('FOUR')

auth = tweepy.OAuthHandler(one, two)
auth.set_access_token(three,four)

## parameters
bristol_code = "E06000023"

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

# check authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# check if there is new bristol data
last_tweet = api.user_timeline(id = "@Bristol_C19", count = 1)[0].text
new_tweet = main(code = bristol_code)

if new_tweet != last_tweet:
  print("#-- New tweet --#")
  print(new_tweet)
  api.update_status(new_tweet)
else: 
  print("#-- No updates --#")
