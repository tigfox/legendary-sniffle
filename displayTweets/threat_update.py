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

tweets = api.user_timeline(screen_name='threat_update', count=1, include_rts=False, exclude_replies=True)
for status in tweets:
    media = status.entities.get('media', [])
    if (len(media) > 0):
        threat_image = media[0]['media_url']
        print(media[0]['media_url'])

webbrowser.open(threat_image)
