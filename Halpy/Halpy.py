#!/usr/bin/env python
#this is the most simplistic irc bot, meant as a first example for simple alerting

import socket
import sys
import time
import requests
from xml.etree import ElementTree

#constants
server = "irc.freenode.org"
channel = "#Synculus"
nick = "junkbot"
alert = ":!halp"
ack = ":!ack"
catsource = "http://thecatapi.com/api/images/get?format=xml&api_key=NjgxMjU&size=full&results_per_page=1&type=gif"

def getCat():
   response = requests.get(catsource)
   tree = ElementTree.fromstring(response.content)
   cat = tree.findtext("./data/images/image/url")
   link = tree.findtext('.data/images/image/source_url')
   return cat

#def connectToServer():
#make a socket
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("connecting to: %s" % server)

#connect
irc.connect((server, 6667))
irc.send("USER %s %s %s :I'm helping!\n" % (nick,nick,nick))
irc.send("NICK %s\n" % nick)

#should be on network now
print ("joined %s" % server)

#connectToServer()
while 1:
    text=irc.recv(2048)
    print text

#once you're on the network, join channel   
    if text.find(':%s MODE' % nick) != -1:
        irc.send("JOIN %s\n" % channel)
        print ("tried to join %s" % channel)

#watch for pings - don't ping timeout
    if text.find('PING') != -1:
        irc.send('PONG %s\r\n' % text.split()[1])
        print "pong"

#watch for halp
    if text.find(alert) != -1:
        t = text.split(alert)
        to = t[1].strip()
        u = text.split('!')
        reporter = u[0].strip()[1:]
        irc.send("PRIVMSG %s :OMG I'll find halp %s! \r\n" % (channel,reporter))
        irc.send('PRIVMSG %s :Please enjoy this cat while I alert the humans: %s \r\n'%(channel,getCat()))
        print "saw halp" #fire off some rockets or something
        print "%s needs halp with %s in %s" % (reporter,str(to),channel)

#convert to danzigs
    if text.find(":!danzig") != -1:
        t = text.split(":!danzig")
        to = t[1].strip() #this is now the found string without the nick
        u = text.split('!') #this is the whole username
        reporter = u[0].strip()[1:] #this is only the nick
        if to.find("meters") != -1:
            string = to.split("meters")
            try:
                amount = float(string[0])
                danzigs = (amount / 2)
                irc.send("PRIVMSG %s :%s, %r meters is %r Danzigs.\r\n" % (channel,reporter,amount,danzigs))
                print "%s meters is %s Danzigs." % (amount,danzigs)
            except ValueError:
                string = to.split("kilometers")
                amount = float(string[0])
                danzigs = (amount / .002)
                irc.send("PRIVMSG %s :%s, %s kilometers is %s Danzigs.\r\n" % (channel,reporter,str(amount),str(danzigs)))
                print "%s kilometers is %s Danzigs." % (str(amount),str(danzigs))
        if to.find("grams") != -1:
            string = to.split("grams")
            try:
                amount = float(string[0])
                danzigs = (amount / 84000)
                irc.send("PRIVMSG %s :%s, %s grams is %s Danzigs.\r\n" % (channel,reporter,str(amount),str(danzigs)))
                print "%s grams is %s Danzigs." % (amount,danzigs)
            except ValueError:
                string = to.split("kilograms")
                amount = float(string[0])
                danzigs = (amount / 84)
                irc.send("PRIVMSG %s :%s, %s kilograms is %s Danzigs.\r\n" % (channel,reporter,str(amount),str(danzigs)))
                print "%s kilograms is %s Danzigs." % (amount,danzigs)

#refuse ops
    if text.find('+o %s' % nick) != -1:
        irc.send('MODE %s -o %s \r\n' % (channel,nick))
        irc.send('PRIVMSG %s :It is probably stupid to op %s \r\n' % (channel,nick))
        print "donut op me pls"

#allow !halp to be acknowledged
    if text.find(':!ack') != -1:
        u = text.split('!')
        acker = u[0].strip()[1:]
        irc.send('PRIVMSG %s :Thanks %s! \r\n' % (channel,acker))
        print "%s ack'd that shit"% acker
