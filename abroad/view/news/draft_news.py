# -*- coding: utf-8 -*-
# @Time    : 2019/5/10 13:30
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *

# 我的草稿
@csrf_exempt
def load_draft_page(request):
    return render(request, "news/draft_news.html", locals())