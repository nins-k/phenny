import httplib
import urllib
import urllib2
import socket
import re
import time
import cPickle

"""
solsms.py - Sending text messages via http://solinked.com
Ninad J. Kulkarni  - nins
nins_b@hotmail.com
"""

def sendmessage(message,phonenumber,countrycode):
    socket.setdefaulttimeout(10)
 
    req_url = "http://slidesms.com/solinked/sentsms.php"

    req_headers = {'Host': 'slidesms.com',\

            'Connection': 'keep-alive',\
            'Cache-Control': 'max-age=0',\
            'Origin': 'http://solinked.com',\

            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5',\

            'Content-Type': 'application/x-www-form-urlencoded',\
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\

            'Referer': 'http://solinked.com/',\

            'Accept-Encoding': 'gzip,deflate,sdch',\
            'Accept-Language': 'en-US,en;q=0.8',\

            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',\
    }

    raw_data = {'country': countrycode,\
            'senderaddress': countrycode+phonenumber,\
            'mymessage': message,\
            'submit':'SEND'}

    req_data = urllib.urlencode(raw_data)
    req = urllib2.Request(req_url,req_data,req_headers)
    
    try:
        resp = urllib2.urlopen(req)
        if(re.search("<title>Message Sent: SoLinked.com",resp.read())!=None):
            return "Message sent successfully via http://solinked.com"
        else:
            return "It seems the message did not go through."
    except IOError, e:
        return e.code +" ; "+e.reason


def solsave(phenny,input):
    """.save yourcountrycode yournumber - saves your phone number for your current nick."""

    insl = input.group().split(" ")
    if len(insl)<3:
        phenny.say(input.nick + ": " + "Not enough parameters.")
    elif len(insl[1])>4:
        phenny.say(input.nick + ": " + "Fake country code.")
    elif not insl[1].isdigit() or not insl[2].isdigit():
        phenny.say(input.nick + ": " + "Use digits only.")
    else:
        phl = load()
        x = 4-len(insl[1])
        insl[1]="0"*x+insl[1]
        nickl = input.nick.lower()
        phl[nickl]=[insl[1],insl[2]]
        save(phl)
        phenny.say(input.nick + ": " + "Your data has been saved.")
    

solsave.example=".save 91 976844XXXX"
solsave.commands=["save"]

def solerase(phenny,input):
    """.erase - removes your current nick and the associated
    phone number from memory."""

    phl = load()
    nickl = input.nick.lower()
    if nickl in phl:
        del phl[nickl]
        save(phl)
        phenny.say(input.nick +": "+ "Your data as been deleted.")
    else:
        phenny.say(input.nick +": "+ "No data present for your nick.")
    
solerase.example=".erase"
solerase.commands=["erase"]

def solsms(phenny,input):
    """.txt nick message - sends the message (285 chars) as a text message
    to 'nick' if s/he has saved his number."""

    insl = input.group().split(" ")
    nickl = insl[1].lower()
    phl = load()
    if nickl in phl and len(insl)>2:
        t = phl[nickl]
        res = sendmessage(input.nick+" - " + input.sender + ":" +\
                    input.group()[6+len(insl[1]):285],t[1],t[0])
        phenny.say(input.nick + ": " + res)
    else:
        phenny.say(input.nick +": " + "No data has been saved for this nick.")
    
solsms.example=".txt nins Get your butt online"
solsms.commands=["txt","sms"]


def save(phlist):
    file = open('phlist.shana','w')
    cPickle.dump(phlist,file)
    file.close()

def load():
    try:
        file = open('phlist.shana','r')
        ret = cPickle.load(file)
        file.close()
    except IOError:
        ret = {}
    return ret


if __name__ == "__main__":
    print __doc__.strip()











    
