import tweepy
import os
from dotenv import load_dotenv
from textblob import TextBlob

# Load .env file and associated vars
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


class Twitter:

    def __init__(self):
        self.api = None

        self.session()

    def session(self, consumer_key=CONSUMER_KEY,
                consumer_secret=CONSUMER_SECRET,
                access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_TOKEN_SECRET
                ):
        # Authentication
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def create_stream_listener(self):
        streamListener = StreamListener()
        return tweepy.Stream(auth=self.api.auth, listener=streamListener)


class StreamListener(tweepy.StreamListener, Twitter):
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
            place = self.api.geo_id(status.place.id)
            location = place.country

### Streaming ###
# twitter_stream = twitter.create_stream_listener()
# twitter_stream.filter(track=['#covid19'], is_async=True)
