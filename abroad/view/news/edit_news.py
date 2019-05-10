# -*- coding: utf-8 -*-
# @Time    : 2019/5/10 13:29
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *

# 编辑文章
@csrf_exempt
def load_edit_page(request):
    return render(request, "news/edit_news.html", locals())