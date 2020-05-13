import json
from random import choice #used for picking ranodm fact and image from array
import tweepy #god bless
import secrets #api tokens
import beefacts #array of bee facts and images

#Create a stream listener to listen for tweets with keywords
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    #When a tweet is received, pull a random fact and tweet back at the user
    def on_status(self, tweet):
        random_fact_array = get_bee_fact()
        random_fact = random_fact_array[0]
        random_image = self.api.media_upload(random_fact_array[1])

        at_user = " @" + tweet.user.screen_name

        reply_with_fact = self.api.update_status(status = random_fact + at_user, media_ids = [random_image.media_id], in_reply_to_staus_id = tweet.id, auto_populate_reply_metadata = True)

        print(f"Succes!")

    #If there's an error, get the status code that Twitter sends over
    def on_error(self, status):
        print(status)

#create an api using the tokens and make sure authentication goees okay
def create_api():
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_secret)

    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api

#super simple function to get the bee facts
def get_bee_fact():
    return choice(beefacts.bee_fact_array)

#cerates the api, creates the listener, and then listens and responds when it sees any keywords
def main(keywords):
    api = create_api()
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["#BeeFactBot", "#beefactBot", "#beeFactbot", "#Beefactbot", "#BeeFactbot", "#beeFactBot", "#BeefactBot"])
