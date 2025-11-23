import requests

class Tweet:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Tweet, cls).__new__(cls)
        return cls._instance

    def make_tweet(self, tweet, user_token):
        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=tweet)
        if response.status_code not in (200, 201):
            raise Exception(f"Error: {response.status_code} {response.text}")
        print("Tweeted:", response.json())
        return response.json()
