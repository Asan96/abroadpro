# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 22:58
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from abroad.models import *
from abroad.view import *
from abroad.views import *

@csrf_exempt
def load_manage_news_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, 'manage/manage_news.html', locals())