#!/usr/bin/env python3

# twitter modules
import tweepy
from tweepy import OAuthHandler

# display modules
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

# and config module
import config

# First we need to get the status we'll eventually display. Basic steps:
# https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

# set up tweepy with creds (you need these in config.py)
auth = OAuthHandler(config.con_key, config.con_sec)
auth.set_access_token(config.acc_key, config.acc_sec)
api = tweepy.API(auth)

# put the text of the most recent tweet into display_text
tweets = api.user_timeline(screen_name='censusAmericans', count=1, include_rts=False, exclude_replies=True)
for status in tweets:
    display_text = status.text


# Once we've got the tweet text, we need to display it.
# Let's use the inkyphat library from pimoroni:
# https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat

# configure the display
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(FredokaOne, 22)
w, h = font.getsize(display_text)
print(w + " by " + h)



