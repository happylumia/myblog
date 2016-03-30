#! /bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello World, Django")
def detail(request, my_args):
    post = Article.objects.all()[int(my_args)]
    str = ("title = %s, category = %s, date_time= %s, content = %s" %(post.tilte, post.category, post.date_time, post.content))
    return HttpResponse(str)

