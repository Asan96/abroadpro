# -*- coding: utf-8 -*-
# @Time    : 2019/5/10 13:29
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *

# 我的推送
@csrf_exempt
def load_push_page(request):
    return render(request, "news/push_news.html", locals())