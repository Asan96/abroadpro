# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth import logout
from models import *

import json


@login_required
@csrf_exempt
def load_base_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, "base.html", locals())


@login_required
@csrf_exempt
def load_note_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, "note/note.html", locals())


@login_required
@csrf_exempt
def load_home_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, "home/home.html", locals())


@csrf_exempt
def log_out(request):
    logout(request)
    result = {'ret': True, 'msg': '登出成功！'}
    return HttpResponse(json.dumps(result), content_type='application/json')


def public_params(request):
    operations = Operating.objects.filter(is_root='1').values()
    now_nickname = request.user.nickname
    user_id = request.user.id
    msg_count = Message.objects.filter(to_user_id=user_id, state='0').count()
    return operations, user_id, msg_count, now_nickname