import os

from requests_oauthlib import OAuth1Session

class Tweet:
    _instance = None

    CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.authenticate()
        return cls._instance

    def authenticate(self):
        # Debug: print environment variables
        print(os.getenv('TWITTER_CONSUMER_KEY'))
        print(os.getenv('TWITTER_CONSUMER_SECRET'))
        print(os.getenv('TWITTER_ACCESS_TOKEN'))
        print(os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

        self.oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=self.ACCESS_TOKEN,
            resource_owner_secret=self.ACCESS_TOKEN_SECRET,
        )

    def make_tweet(self, tweet):
        if hasattr(self, 'oauth'):
            response = self.oauth.post(
                "https://api.twitter.com/2/tweets",
                json=tweet,
            )
            if response.status_code not in (200, 201):
                raise Exception(f"Error: {response.status_code} {response.text}")
            print("Tweeted:", response.json())
        else:
            raise ValueError("Authentication failed!")
