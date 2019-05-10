# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 19:43
# @Author  : wangluchao
import json
import base64
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import User
from abroad.view import MyEmail
from django.utils import timezone

def login_page_load(request):
    return render(request, "login/login.html", locals())


@csrf_exempt
def login_verify(request):
    params = request.POST.dict()
    user_id = params.get('user_id', '')
    password = params.get('password', '')
    UserObj = User.objects.filter(user_id=user_id, password=base64.b64encode(password))
    if UserObj:
        return HttpResponse(json.dumps({'ret': True, 'msg': '登录成功！'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'ret': False, 'msg': '账号或密码错误，若无账号请先注册！'}), content_type='application/json')


@csrf_exempt
def login_register(request):
    params = request.POST.dict()
    user_id = params.get('user_id', '')
    first_password = params.get('first_password', '')
    username = params.get('user_name', '')
    birthday = params.get('birthday', '')
    sex = params.get('sex', '')
    email = params.get('email', '')
    now_time =timezone.now()
    userObj = User.objects
    check_user_id = userObj.filter(user_id=user_id)
    check_username = userObj.filter(username=username)
    check_email = userObj.filter(email=email)
    if check_user_id:
        return HttpResponse(json.dumps({'ret': False, 'msg': '用户名已存在！'}), content_type='application/json')
    elif check_username:
        return HttpResponse(json.dumps({'ret': False, 'msg': '账号已存在！'}), content_type='application/json')
    elif check_email:
        return HttpResponse(json.dumps({'ret': False, 'msg': '邮箱已被使用！'}), content_type='application/json')
    else:
        user_dict = {
            'user_id': user_id,
            'username': username,
            'password': base64.b64encode(first_password),
            'email': email,
            'create_time': now_time,
            'update_time': now_time,
        }
        if sex:
            user_dict['sex'] = sex
        if birthday:
            user_dict['birthday'] = birthday
        userObj.create(**user_dict)
        return HttpResponse(json.dumps({'ret': True, 'msg': '注册成功！'}), content_type='application/json')

@csrf_exempt
def send_verify_msg(request):
    params = request.POST.dict()
    verify_msg = str(random.randint(100000, 999999))
    user_id = params['user_id']
    email = params['email']
    userObj = User.objects.filter(user_id=user_id, email=email)
    if userObj:
        content = '您的账号： '+str(user_id)+' 验证码为：'+verify_msg
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
    user_id = params['user_id']
    email = params['email']
    verify_msg = params['verify_msg']
    info = User.objects.filter(user_id=user_id, email=email).values('verify_msg').first()
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
    query_dict = {
        'user_id': params['user_id'],
        'email': params['email'],
        'verify_msg': params['verify_msg']
    }
    password = params['password']
    userObj = User.objects.filter(**query_dict)
    if userObj:
        userObj.update(password=base64.b64encode(password), update_time=timezone.now())
        return HttpResponse(json.dumps({'ret': True, 'msg': '密码修改成功！'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'ret': False, 'msg': '输入信息有误，无法修改密码！'}), content_type='application/json')

