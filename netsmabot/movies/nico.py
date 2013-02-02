#!/usr/bin/python2.5
# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
import datetime
import urllib2
import re

class Entry:
    def __init__(self, entry):
        self.url = entry[0].decode('utf-8')
        self.title = entry[1].decode('utf-8')
        self.date = entry[2]


def get_post(html):
    """ get new videos from posted video list page in the community """
    soup = BeautifulSoup(html)

    videos = [[_a.get('href'), _a.renderContents()] for _a in soup('a', {'class':'video'})]
    p =  soup('p', {'class': 'videoDate'})
    num = re.compile(u"(\d+)\D+")

    for id, i in enumerate(p):
        posted_date_tag = BeautifulSoup(i.renderContents())
        yyyydddd = [yd.renderContents().strip() for yd in posted_date_tag('strong')] 
        time = [t.renderContents().strip() for t in posted_date_tag('span', {'class': 'optional'})] 

        for yd in yyyydddd: 
            year, month, date = [int(x) for x in num.split(yd) if not x is '']
        for t in time: 
            hour, min, sec = [int(x) for x in num.split(t) if not x is '']

        posted_datetime = datetime.datetime(year, month, date, hour, min)
        videos[id].append(posted_datetime)

    entrylist = [Entry(e) for e in videos]
    return entrylist


def get_all_post():
    posts = []
    coList = ['161644', '1391815']
    for co in coList:
        pid = 1
        while True:
            html = urllib2.urlopen('http://com.nicovideo.jp/video/co%s?page=%d&order=d' % (co, pid)).read()
            entries = get_post(html)
            if len(entries) == 0: break
            posts += entries
            pid += 1
    return posts

if __name__ == "__main__":
    get_all_post()
