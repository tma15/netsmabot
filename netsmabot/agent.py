#!/usr/bin/python
#-*- coding:utf-8 -*-
import urllib2
from time import sleep

url = 'http://netsmabot-tma15.dotcloud.com/'
#while True:
try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open(url)
    html.close()
    opener.close()
except urllib2.URLError, e:
    print e
#    sleep(60)
