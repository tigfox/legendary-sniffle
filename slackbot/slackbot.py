#!/usr/bin/env python

from slackclient import SlackClient
import config

token = config.token
sc = SlackClient(token)

aj = "U11EYH86P"
bwoe = "U11C97QAH"
franson = "U11CQA649"
jappel = "U11CPG866"
general = "C11C8GH5M"

def sendMsg(sendTo, msgTxt):
    print sc.api_call("chat.postMessage", channel=sendTo, username="Yo Mama's Peg Leg", text=msgTxt)

#print sc.api_call("im.history", channel="D11B3EHTM")

sendMsg(general, "")

