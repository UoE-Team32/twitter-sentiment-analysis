import tweepy
import os
from dotenv import load_dotenv

# Load .env file and associated vars
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_status(self, status):
        # Only filter tweets containing English language
        if status.lang != "en":
            return

        # Check there is the place attribute
        # Quick hack to set location
        location = "N/A"
        if hasattr(status.place, 'id'):
            place = api.geo_id(status.place.id)
            location = place.country

        # Analyse the tweet
        analysis = TextBlob(status.text)
        if analysis.sentiment.polarity > 0: 
            print('ID: ' + status.id_str + ', Polarity: Positive, Location: ' + location)
        elif analysis.sentiment.polarity == 0: 
            print('ID: ' + status.id_str + ', Polarity: Neutral, Location: ' + location)
        else: 
            print('ID: ' + status.id_str + ', Polarity: Negative, Location: ' + location)

def create_session():
    streamListener = StreamListener()
    return tweepy.Stream(auth=api.auth, listener=streamListener)
