import os
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect, render
from django.http import HttpResponse

TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID')
TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET')
TWITTER_REDIRECT_URI = os.getenv('TWITTER_REDIRECT_URI')
TWITTER_SCOPE = ['tweet.read', 'tweet.write', 'users.read', 'offline.access']

def twitter_login(request):
    oauth = OAuth2Session(
        TWITTER_CLIENT_ID,
        redirect_uri=TWITTER_REDIRECT_URI,
        scope=TWITTER_SCOPE
    )
    authorization_url, state = oauth.authorization_url(
        'https://twitter.com/i/oauth2/authorize',
        code_challenge_method='plain'
    )
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def twitter_callback(request):
    oauth = OAuth2Session(
        TWITTER_CLIENT_ID,
        redirect_uri=TWITTER_REDIRECT_URI,
        scope=TWITTER_SCOPE
    )
    code = request.GET.get('code')
    token = oauth.fetch_token(
        'https://api.twitter.com/2/oauth2/token',
        client_secret=TWITTER_CLIENT_SECRET,
        code=code
    )
    # Save user's access token for future posting
    request.session['twitter_access_token'] = token['access_token']
    return HttpResponse("Twitter authorized! You may now add a store.")
