#!/usr/bin/env python

from slackclient import SlackClient
import config

token = config.token
sc = SlackClient(token)
chan = "C11C8GH5M"
greeting = "still only 10 lines, though not especially interactive. But not bad for 15 minutes of research."
print sc.api_call("chat.postMessage", channel=chan, username="Yo Mama's Peg Leg", text=greeting)
