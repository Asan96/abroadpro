# -*- coding: utf-8 -*-
# @Time    : 2019/5/10 13:30
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *

# 注意事项
@csrf_exempt
def load_note_page(request):
    return render(request, "news/note_news.html", locals())