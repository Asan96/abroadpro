# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth import logout
from models import *

import json


@csrf_exempt
def page_init(request):
    operations = Operating.objects.values()
    now_nickname = request.user.nickname
    return operations, now_nickname


@login_required
@csrf_exempt
def load_base_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "base.html", locals())

@login_required
@csrf_exempt
def load_home_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "home/home.html", locals())

@csrf_exempt
def log_out(request):
    logout(request)
    result = {'ret': True, 'msg': '登出成功！'}
    return HttpResponse(json.dumps(result), content_type='application/json')