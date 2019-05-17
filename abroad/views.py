# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from models import *


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