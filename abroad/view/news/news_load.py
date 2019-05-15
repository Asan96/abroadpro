# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:39
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *
from django.contrib.auth.decorators import login_required


@login_required
@csrf_exempt
def load_news_page(request):
    operations = Operating.objects.values()
    return render(request, "news/news.html", locals())

@login_required
@csrf_exempt
def load_browsing_page(request):
    operations = Operating.objects.values()
    params = request.GET.dict()
    nickname = params['nickname']
    title = params['title']
    user_id = User.objects.filter(nickname=nickname).values_list('id', flat=True).first()
    new = News.objects.filter(user_id=user_id, title=title).first()
    return render(request, "news/browsing_news.html", locals())