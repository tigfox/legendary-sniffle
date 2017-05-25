#!/usr/bin/env python

import socket
import sys
import requests
import time
from xml.etree import ElementTree
import config

"""class for irc server connection - this handles joining the server, responding to pings
      needs to have a single nick, single irc server
      that way you have a server object that will include channel objects, which can each include help-request objects?
      stream needs to live in the server instance, and can parcel out alerts to channels?
"""
class ircServer:
    'Class for irc server connection, requires server address, server port, nick. Provides ircServer.stream which is the socket to the irc server'
    
    def __init__(self, addr, port, nick, realname):
        self.addr = addr
        self.port = port
        self.nick = nick
        self.realname = realname
        self.log = [ '/tmp/%s/%s'%(self.addr, self.nick) ]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("connecting to: %s" % self.addr)
        self.server.connect((self.addr, self.port))
        self.server.setblocking(False)
        self.server.send("USER %s %s %s :%s\n" % (self.nick,self.nick,self.nick, self.realname))
        self.server.send("NICK %s\n" % self.nick)
        self.log_append = []
        for i, tail in enumerate(self.log):
            self.log_append.append('')

        while 1:
            self.stream = self.server.recv(2048)
            if self.stream.find(':%s MODE' % self.nick) != -1: #means we're on the network
                self.connected = True
            #need to parse the stream here, into channels (PRIVMSG #channel)
            #does the server keep track of what channels it's in? 
            #No - if you receive a PRIVMSG just assume you're in that channel
#PMs (PRIVMSG self.nick)(spawn a PM object?), server pings

"""class for irc channel - handles joining the channel, what the alert words are
      single irc socket, single channel, single alert word, action to take when alert is seen
"""
class channel:
    'Class for irc channel inside a server. requires server obj, channel name, alertWord. Receives events from server. Listens for, creates and closes alerts.'
    def __init__(self, server, chanName, alertWord):
        self.server = server
        self.chan = chanName
        self.alertWord = alertWord
        
    def join_channel():
        if self.server:
            self.server.stream.send('JOIN %s\r\n'%self.chan)

    def part_channel(message="l8r sk8r"):
        if self.server:
            self.server.stream.send('PART %s %s\r\n'%(self.chan, message))
            del self.alertWord
            del self.chan
            del self.server
        #some way to close child alerts? - give each alert a random number and add it to an array? creating an alert passes it that as an id?xc

    def in_message(message_text):
        #regex ^:$user\!.*( PRIVMSG )$chan\ :$msg

"""class for alert
      single user(creator), text of alert, 
"""
class alert:
    'Class for alerts. Alerts are specific to a channel or user. requires creator, channel(or nick)'
    def __init__(self, creator, channel):
        self.creator = creator
        self.channel = channel

"""I mean, who doesn't need cats?
"""
def getCat():
   response = requests.get(config.catsource)
   tree = ElementTree.fromstring(response.content)
   cat = tree.findtext("./data/images/image/url")
   link = tree.findtext('.data/images/image/source_url')
   return cat

if __name__ == '__main__':

    server1 = ircServer(config.server, "6667", config.nick)
    chan1 = channel(config.channel, config.channel, config.alert)
