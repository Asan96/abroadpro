# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 19:43
# @Author  : wangluchao
import json
import base64
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *
from abroad.view import MyEmail
from django.utils import timezone
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth import get_user_model

def login_page_load(request):
    countrys = Location.objects.filter(level='2')
    return render(request, "login/login.html", locals())


@csrf_exempt
def login_verify(request):
    params = request.POST.dict()
    username = params.get('user_id', '')
    password = params.get('password', '')
    UserObj = auth.authenticate(username=username, password=password)
    if UserObj:
        auth.login(request, UserObj)
        return HttpResponse(json.dumps({'ret': True, 'msg': '登陆成功'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'ret': False, 'msg': '账号或密码错误，若无账号请先注册！'}), content_type='application/json')


@csrf_exempt
def login_register(request):
    params = request.POST.dict()
    username = params.get('user_id', '')
    first_password = params.get('first_password', '')
    nickname = params.get('user_name', '')
    birthday = params.get('birthday', '')
    sex = params.get('sex', '')
    email = params.get('email', '')
    country = params['country']
    school = params['school']
    now_time =timezone.now()
    userObj = User.objects
    check_username = userObj.filter(username=username)
    check_nickname = userObj.filter(nickname=nickname)
    check_email = userObj.filter(email=email)
    if check_username:
        return HttpResponse(json.dumps({'ret': False, 'msg': '用户名已存在！'}), content_type='application/json')
    elif check_nickname:
        return HttpResponse(json.dumps({'ret': False, 'msg': '账号已存在！'}), content_type='application/json')
    elif check_email:
        return HttpResponse(json.dumps({'ret': False, 'msg': '邮箱已被使用！'}), content_type='application/json')
    else:
        user_dict = {
            'username': username,
            'nickname': nickname,
            'password': first_password,
            'email': email,
            'country': country,
            'school': school,
            'date_joined': now_time,
            'update_time': now_time,
        }
        if sex:
            user_dict['sex'] = sex
        if birthday:
            user_dict['birthday'] = birthday
        userObj.create_user(**user_dict)
        return HttpResponse(json.dumps({'ret': True, 'msg': '注册成功！'}), content_type='application/json')

@csrf_exempt
def send_verify_msg(request):
    params = request.POST.dict()
    verify_msg = str(random.randint(100000, 999999))
    username = params['user_id']
    email = params['email']
    userObj = User.objects.filter(username=username, email=email)
    if userObj:
        content = '您的账号： '+str(username)+' 验证码为：'+verify_msg
        userObj.update(verify_msg=verify_msg)
        MyEmail(
            to_list=[email],
            content={
                'content': content,
                'type': 'plain',
                'coding': 'utf-8'
            }
        ).send()
        return HttpResponse(json.dumps({'ret': True, 'msg': '验证码已发送！'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'ret': False, 'msg': '账号与邮箱不匹配！'}), content_type='application/json')

@csrf_exempt
def check_verify_msg(request):
    params = request.POST.dict()
    username = params['user_id']
    email = params['email']
    verify_msg = params['verify_msg']
    info = User.objects.filter(username=username, email=email).values('verify_msg').first()
    if info:
        if info['verify_msg'] == verify_msg:
            return HttpResponse(json.dumps({'ret': True, 'msg': '验证码正确！'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'ret': False, 'msg': '验证码错误！'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'ret': False, 'msg': '账号、邮箱信息填写有误！'}), content_type='application/json')

@csrf_exempt
def modify_password(request):
    params = request.POST.dict()
    username = params['user_id']
    password = params['password']
    query_dict = {
        'username': username,
        'email': params['email'],
        'verify_msg': params['verify_msg']
    }
    userObj = User.objects.filter(**query_dict)
    if userObj:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        userObj.update(update_time=timezone.now())
        return HttpResponse(json.dumps({'ret': True, 'msg': '密码修改成功！'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'ret': False, 'msg': '输入信息有误，无法修改密码！'}), content_type='application/json')

