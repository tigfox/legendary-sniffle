#!/usr/bin/env python3

import tweepy
from tweepy import OAuthHandler
import webbrowser
import config

auth = OAuthHandler(config.con_key, config.con_sec)
auth.set_access_token(config.acc_key, config.acc_sec)

api = tweepy.API(auth)


#for status in tweepy.Cursor(api.home_timeline).items(1):
#    print(status.text)
#    print(api.home_timeline)

tweets = api.user_timeline(screen_name='censusAmericans', count=1, include_rts=False, exclude_replies=True)
for status in tweets:
    print(status.text)
#    text = status.entities.get('text', [])
#    if (len(text) > 0):
#        print(text)

