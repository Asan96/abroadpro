# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:39
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *

@csrf_exempt
def load_communicate_page(request):
    operations = Operating.objects.values()
    return render(request, "communicate/communicate.html", locals())