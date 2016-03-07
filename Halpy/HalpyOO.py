import socket
import sys
import time
import requests
from xml.etree import ElementTree

#constants
server = "irc.etsycorp.com"
channel = "#SquirrelOps"
nick = "Halpy"
alert = ":!halp"
ack = ":!ack"
catsource = "http://thecatapi.com/api/images/get?format=xml&api_key=NjgxMjU&size=full&results_per_page=1"

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
   text=irc.recv(2040)
   print text

#once you're on the network, join channel   
   if text.find(':Halpy MODE') != -1:
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
       irc.send('PRIVMSG %s :OMG Finding halp %s! \r\n' % (channel,reporter))
       irc.send('PRIVMSG %s :Please enjoy this cat picture while I alert the humans: %s \r\n'%(channel,getCat()))
       print "saw halp" #fire off some rockets or something
       print "%s needs halp with %s in %s" % (reporter,str(to),channel)

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
