# NOTE: You should have your own Twitter developer crednetials to run this program

# Fill this in with your proprietary credentials
passwords = {'API_Key':'',
            'API_Secret':'',
            'Access_Token':'',
            'Access_Secret':''}

# IMPORTS
import tweepy
import datetime
from rpy2.robjects.packages import importr
import random

# API SETUP
## Credentials for this app are stored in a private dictionary
authSet = tweepy.OAuthHandler(consumer_key = passwords['API_Key'],
                              consumer_secret= passwords['API_Secret'])

authSet.set_access_token(key = passwords['Access_Token'],
                         secret = passwords['Access_Secret'])

api = tweepy.API(authSet, wait_on_rate_limit = True)

# Check to confirm credentials
try:
    api.verify_credentials()
    print("\nConfirmed: Valid Credentials\n")

except:
    print("\nWhoops! Invalid credentials\n")

# Imports "praise" package from R ... generates random praise!
def tweetGenerator():

    # Generate random praise and strip it down to just text
    praise = importr("praise")
    nice = str(praise.praise())[5:-2]

    # Some random nice phrases to tag on to the tweet
    addOnPhrases = ['Make today count', 'Do something nice for yourself today', 'I believe in you',
                   'You can do it!', 'Be great today', 'Make today great', 'You matter!', 'Take a breath']

    random.shuffle(addOnPhrases)
    phrase = random.choice(addOnPhrases)

    # Combine the two sentiments
    tweet = str(nice + " " + phrase)
    return tweet

# TWEETS! Updates Twitter timeline using helper method
def spreadTheLove():

    tweet = tweetGenerator()
    api.update_status(tweet)

# Follows accounts that have recently tweeted positive things
def getFollowers():

    # We'll search for a few buzzwords ...
    newGuys = []
    buzzwords = ['happy', 'positive', 'love']

    for word in buzzwords:

        # Search for 10 tweets from each buzzword, add Twitter handles to newGuys list
        for tweet in tweepy.Cursor(api.search, q = word + " -filter:mentions -filter:links -filter:retweets",
                                  lang = 'en', tweet_mode = 'extended', result_type = 'recent').items(10):

            newGuys.append(tweet.user.screen_name)

    # Follow each account
    for friendo in newGuys:
        api.create_friendship(friendo)

    print("Congrats on your new friends!")


# Get today's date in weekday form
today = (datetime.datetime.now()).strftime("%A")

# We'll only follow new users on Wednesdays and Fridays
followerDays = ["Wednesday", "Friday"]

if today in followerDays:

    getFollowers()

# We'll tweet everyday!
spreadTheLove()
