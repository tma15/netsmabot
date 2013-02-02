#!/usr/bin/python
#-*- coding:utf8 -*-
import re
import os
import sys
import yaml
import urllib
import socket
import BeautifulSoup
from twitter import Twitter, OAuth

def owner_name(co):
    community_url = 'http://com.nicovideo.jp/community/%s' % co
    html = urllib.urlopen(community_url)
    soup = BeautifulSoup.BeautifulSoup(html)
    htmlfile = str(soup).splitlines()
    for line in htmlfile:
        if re.compile('オーナー：').search(line):
            owner = BeautifulSoup.BeautifulSoup(line)
            owner_name = owner.find('strong').renderContents()
            return owner_name
    return ''

def full_title(lv):
    live = 'http://live.nicovideo.jp/watch/lv%s' % lv
    html = urllib.urlopen(live)
    soup = BeautifulSoup.BeautifulSoup(html)
    try:
        title = soup.findAll('span', {'itemprop': 'name'})[0].renderContents()
        return title
    except:
        return ''

yml = os.path.join('config.yaml')
CONFIG = yaml.load(open(yml))

url = 'https://secure.nicovideo.jp/secure/login?site=nicolive_antenna'
mail = CONFIG['mail']
password = CONFIG['password']
params = urllib.urlencode({'mail': mail, 'password': password})

f = urllib.urlopen(url, params)

s = BeautifulSoup.BeautifulSoup(f.read())
ticket = s.find('ticket').renderContents()
url = 'http://live.nicovideo.jp/api/getalertstatus'
params = urllib.urlencode({'ticket': ticket})
f = urllib.urlopen(url, params)

s = BeautifulSoup.BeautifulSoup(f.read())
getalertstatus = s.find('getalertstatus')
addr = getalertstatus.find('addr').renderContents()
port = int(getalertstatus.find('port').renderContents())
thread = int(getalertstatus.find('thread').renderContents())

community_id_set = {'プリンス': 'co1391815',
                    'RED': 'co571730',
                    'たつまん': 'co310531',
                    'ぶちまけ祭り（アニキ）': 'co1038007',
                    'えりたん': 'co334937',
                    '段位戦': 'co161644',
                    'ネスボ': 'co542375',
                    'ふぁうたん': 'co80658',
                    'オリオン': 'co1169807',
                    'sekirei': 'co1337403',
                    '丼プリン': 'co1219761',
                    'とかち': 'co583918',
                    '南国': 'co520657',
                    'J-SNAKE': 'co1532223',
                    }

a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a.connect((addr, port))
a.send('<thread thread="%d" version="20061206" res_from="-1"/>\0' % thread)


while 1:
    d = a.recv(4096)
    s = BeautifulSoup.BeautifulSoup(d)
    chat = s.find('chat')
    try:
        thread = chat.renderContents()
        thread = thread.split(',')
        if len(thread) == 3:
            lv, co, userid = thread
            if co in community_id_set.values():
                lv, co, userid = thread
                url = 'http://live.nicovideo.jp/api/getstreaminfo/lv' + lv
                f = urllib.urlopen(url)
                streaminfo = BeautifulSoup.BeautifulSoup(f.read())
                community_name = streaminfo.find('name').renderContents()

                owner = owner_name(co)
                title = full_title(lv)
                if title == '': title = streaminfo.find('title').renderContents()
                if owner == '':
                    st = '【生放送】%s で %s が開始されました http://live.nicovideo.jp/watch/lv%s' % (community_name, title, lv)
                else:
                    st = '【生放送】%s さんが %s で %s を開始しました http://live.nicovideo.jp/watch/lv%s' % (owner, community_name, title, lv)
                print st
                twitter = Twitter(auth=OAuth(consumer_key=CONFIG['Consumerkey'],
                                            consumer_secret=CONFIG['Consumersecret'],
                                            token=CONFIG['Accesstoken'],
                                            token_secret=CONFIG['Accesstokensecret']))
                twitter.statuses.update(status=st)
    except:
        pass
