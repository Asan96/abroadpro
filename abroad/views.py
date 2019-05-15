# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from models import *

@login_required
@csrf_exempt
def load_base_page(request):
    operations = Operating.objects.values()
    return render(request, "base.html", locals())

@login_required
@csrf_exempt
def load_home_page(request):
    operations = Operating.objects.values()
    return render(request, "home/home.html", locals())