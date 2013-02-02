# Create your views here.
#-*- coding:utf8 -*-
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'netsmabot.settings'
import sys
import yaml
import nico
import models
from django.http import HttpResponse
from subprocess import Popen
from twitter import Twitter, OAuth

def nico_movie(request):
    html = '<html>'
    entries = sorted(nico.get_all_post(), key=lambda x: x.date)
    for e in entries:
        posted_titlelist = [m.title for m in models.Movie.objects.all()]
        if e.title in posted_titlelist: pass
        else:
            m = models.Movie(title=e.title, url=e.url, date=e.date)
            m.save()
            content = e.date.strftime('%Y/%m/%d') + ' ' + e.title + ' ' + e.url
            twitter = Twitter(auth=OAuth(consumer_key=config['Consumerkey'],
                                    consumer_secret=config['Consumersecret'],
                                    token=config['Accesstoken'],
                                    token_secret=config['Accesstokensecret']))
            twitter.statuses.update(status=content)
#            break

    return HttpResponse(html)

if __name__ == "__main__":
    nico_movie(None)
