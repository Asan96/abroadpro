# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from models import *


@csrf_exempt
def load_base_page(request):
    operations = Operating.objects.values()
    return render(request, "base.html", locals())
