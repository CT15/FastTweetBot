import tweepy
from keys_tokens import TW_API_KEY, TW_API_SECRET_KEY, TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(TW_API_KEY, TW_API_SECRET_KEY)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
