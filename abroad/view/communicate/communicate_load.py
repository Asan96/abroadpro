# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:39
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from abroad.models import *
from abroad.view import *


def public_params(request):
    operations = Operating.objects.values()
    user_id = request.user.id
    msg_count = Message.objects.filter(to_user_id=user_id, state='0').count()
    return operations, user_id, msg_count

@login_required
@csrf_exempt
def load_communicate_page(request):
    operations, user_id, msg_count = public_params(request)
    return render(request, "communicate/communicate.html", locals())


@login_required
@csrf_exempt
def load_add_friend_page(request):
    operations, user_id, msg_count = public_params(request)
    return render(request, "communicate/add_friend.html", locals())


@login_required
@csrf_exempt
def load_my_friend_page(request):
    operations, user_id, msg_count = public_params(request)
    return render(request, "communicate/my_friend.html", locals())


@login_required
@csrf_exempt
def load_note_communicate_page(request):
    operations, user_id, msg_count = public_params(request)
    return render(request, "communicate/note_communicate.html", locals())


@login_required
@csrf_exempt
def load_browsing_page(request):
    operations, user_id, msg_count = public_params(request)
    params = request.GET.dict()
    msg_id = params['msg_id']
    msgObj = Message.objects.filter(id=msg_id).first()
    create_time = time_format(msgObj.create_time)
    nickname = User.objects.filter(id=msgObj.from_user_id).values_list('nickname', flat=True).first()
    return render(request, "communicate/browsing_message.html", locals())