# NOTE: You should have your own Twitter developer crednetials to run this program

# ----------------------------------- IMPORTS -----------------------------------

import tweepy
import datetime
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import random
import json

# ----------------------------------- API SETUP -----------------------------------

# NOTE: Credentials for this app are stored in a private dictionary

with open("PASSWORDS.txt") as json_file:

        passwords = json.load(json_file)

authSet = tweepy.OAuthHandler(consumer_key = passwords['API_Key'],      # Set up authorization
                              consumer_secret= passwords['API_Secret'])

authSet.set_access_token(key = passwords['Access_Token'],
                         secret = passwords['Access_Secret'])

api = tweepy.API(authSet, wait_on_rate_limit = True)                    # Set up API connection


try:                                                                    # Check credentials
    api.verify_credentials()

except:
    print("\nWhoops! Invalid credentials\n")

# ----------------------------------- GENERATOR -----------------------------------

# Imports "praise" package from R, concatenates with manually written words of affirmation

def tweetGenerator():

    try:
        praise = importr("praise")

    except:
        utils = importr("utils")
        utils.install_packages("praise", repos='https://cloud.r-project.org')
        praise = importr("praise")

    niceThings = []                                                     # Empty list to concatenate into

    # Included to avoid repetitive phrases
    for i in range(1,10):

        nice = praise.praise()
        niceThings.append(nice)                                         # Add object to list

    random.shuffle(niceThings)                                          # Shuffle list
    nice = str(random.choice(niceThings))[5:-2]                         # Cut off extraneous bits of the string

    # Some random nice phrases to tag on to the tweet
    addOnPhrases = ['Make today count', 'Do something nice for yourself today',
    'I believe in you','You can do it!', 'Be great today', 'Make today great',
    'You matter!', 'Take a breath','You can accomplish anything you set your mind to!',
    'Everyone needs a friend like you','You are a light everywhere you go!',
    'Thank you for being you!','You have a heart of gold','You are absolute magic',
    'Be gentle with yourself, you\'re doing the best you can!']

    random.shuffle(addOnPhrases)
    phrase = random.choice(addOnPhrases)

    tweet = str(nice + " " + phrase)                                    # Combine both sentiments into one string
    return tweet

# ----------------------------------- TWEET SENTIMENTS -----------------------------------

def spreadTheLove():

    tweet = tweetGenerator()
    api.update_status(tweet)

# ----------------------------------- POSITIVE TWITTER USERS -----------------------------------

def friendsList(VOLUME):
    buzzwords = ['happy', 'positive', 'love']                           # Buzzwords to search
    newGuys = []                                                        # Empty list to concatenate into

    for word in buzzwords:

        # Search for 10 tweets from each buzzword, add Twitter handles to newGuys list
        for tweet in tweepy.Cursor(api.search, q = word + " -filter:mentions -filter:links -filter:retweets",
                                  lang = 'en', tweet_mode = 'extended', result_type = 'recent').items(VOLUME):

            newGuys.append(tweet.user.screen_name)                      # Add positive Twitter users to list

    return newGuys

# ----------------------------------- ADD NEW FOLLOWERS -----------------------------------

def makeNewFriends():
    today = (datetime.datetime.now()).strftime("%A")                        # Current day of the week
    followerDays = ["Monday", "Wednesday", "Friday"]                        # Days to obtain new followers

    if today in followerDays:

        friends = friendsList(25)                                           # Assign positive Twiter users to list object

        for friend in friends:                                              # Add positive Twitter users to following list
            api.create_friendship(friend)


# ----------------------------------- HEY HOWDY -----------------------------------

def sayHi():

    friends = friendsList(10)
    praise = importr("praise")
    second_all = []

    # Included to avoid repetitive phrases
    for i in range(1,10):

        nice = praise.praise()
        second_all.append(nice)                                             # Add object to list

    first_all = ["Hey howdy!", "What's up!"]
    third_all = ["Hope you have a great day!", "Make today a good one!",
            "Thanks for being you!", "This world is lucky to have you!"]

    for contact in friends:

        first_pick = (random.choice(first_all))
        second_pick = str(random.choice(second_all))[5:-2]
        third_pick = (random.choice(third_all))

        # Format text before sending tweet
        tweet = "@" + str(contact) + " " + first_pick + " " + second_pick + " " + third_pick

        api.update_status(tweet)                                            # Send tweet


# ----------------------------------- DAILY -----------------------------------

if __name__ == "__main__":

    spreadTheLove()                                                         # Send a tweet
    makeNewFriends()                                                        # Add new followers
    sayHi()                                                                 # Tweet at positive Twitter users

    print("\n *** TWEET SENT ***\n")
    print("Make it a great day!\n")
