'''
Created on Sep 28, 2016

@author: Collin Smith | collinsmith70@gmail.com
'''

import re
import sys
import tweepy
import itertools
import urllib2
import urlparse
import time

from codes import *

filename = 'pokearcadia2.csv'
subregex = "(?<=\dam|\dpm).+\. #PokemonGo #PokeArcadia "
twitterhandle = "pokearcadia"
skipIdsLessThan = 781384100305186816

g_since_id = 0
f = open(filename, 'w')

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page

def process_status(status):
    try:
        #print status
        text = status.text
        text = re.sub("A wild ", "", text)
        text = re.sub(" has appeared in .+! Available until ", ",", text)
        text = re.sub(subregex, ",", text)
        tmp = text.split(",")
        pokemon = tmp[0]
        time = str(status.created_at)
        url = tmp[2]

        url = str(status._json)
        #print url
        url = re.search(re.escape("http://maps.google.com/maps?q=") + "\-?\d+\.\d+,\-?\d+\.\d+", url)
        url = str(url.group())
        #print url
        
        #req = urllib2.Request(url)
        #res = urllib2.urlopen(req)
        #finalurl = res.geturl()
        location = urlparse.urlparse(url).query
        #location = re.sub("/maps", "", location)
        #location = re.sub("/.*", "", location)
        location = re.sub("q=", "", location)
        tmp = location.split(",")
        longitude = tmp[0]
        latitude = tmp[1]
        f.write(str(status.id) + "," + pokemon + "," + time + "," + longitude + "," + latitude + "," + url + "\n")
        f.flush()
        #print "[" + str(status.id) + "] " + pokemon + " until " + time + " at " + longitude + ", " + latitude
    except urllib2.HTTPError as err:
        print "Unexpected error accessing " + url + ": HTTP " + str(err.code) + ": " + err.msg
    except:
        print "Unexpected error: " + str(sys.exc_info()[0])
        print "  while parsing: " + status.text.encode('ascii', 'ignore')
        
    return

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.user_timeline, screen_name=twitterhandle).items():
    if status.id <= skipIdsLessThan:
        break
        
    process_status(status)
    time.sleep(6)

f.close()