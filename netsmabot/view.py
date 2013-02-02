#-*- coding:utf8 -*-
from django.http import HttpResponse

def home(request):
    return HttpResponse('Home<br><a href="./hello">test</a>')


def hello(request):
    return HttpResponse('Hello world<br><a href="../">test</a>')


