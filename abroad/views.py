# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth import logout
from models import *
from abroad.view import *

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
    school = request.user.school
    user_id = request.user.id
    country = request.user.country
    empty_lst = []
    recommend_lst = []
    NewsObj = News.objects.filter(state=1)
    recommendNews = NewsObj.filter(keyword__icontains=school).exclude(user_id=user_id).order_by('-push_time')

    school_count = recommendNews.count()
    if 0 < school_count <= 5:
        for news in recommendNews:
            news_nickname = User.objects.filter(id=news.user_id).values_list('nickname', flat=True).first()
            recommend_dic = {
                'news_id': news.id,
                'title': news.title,
                'article': news.article,
                'news_nickname': news_nickname,
                'keyword': news.keyword,
                'push_time': time_format(news.push_time),
            }
            recommend_lst.append(recommend_dic)
        other_recommendNews = NewsObj.filter(keyword__icontains=country).exclude(user_id=user_id).order_by('-push_time')
        if other_recommendNews.count() > 5-len(recommend_lst):
            other_recommendNews = other_recommendNews[:5-len(recommend_lst)]
            for news in other_recommendNews:
                news_nickname = User.objects.filter(id=news.user_id).values_list('nickname', flat=True).first()
                recommend_dic = {
                    'news_id': news.id,
                    'title': news.title,
                    'article': news.article,
                    'news_nickname': news_nickname,
                    'keyword': news.keyword,
                    'push_time': time_format(news.push_time),
                }
                recommend_lst.append(recommend_dic)
    elif school_count > 5:
        for news in recommendNews[:5]:
            news_nickname = User.objects.filter(id=news.user_id).values_list('nickname', flat=True).first()
            recommend_dic = {
                'news_id': news.id,
                'title': news.title,
                'article': news.article,
                'news_nickname': news_nickname,
                'keyword': news.keyword,
                'push_time': time_format(news.push_time),
            }
            recommend_lst.append(recommend_dic)
    elif not recommendNews:
        recommendNews = NewsObj.filter(keyword__icontains=country).exclude(user_id=user_id).order_by('-push_time')
        if not recommendNews:
            recommendNews = NewsObj.exclude(user_id=user_id).order_by('-push_time')
        if recommendNews.count() > 5:
            recommendNews = recommendNews[:5]
        for news in recommendNews:
            news_nickname = User.objects.filter(id=news.user_id).values_list('nickname', flat=True).first()
            recommend_dic = {
                'news_id': news.id,
                'title': news.title,
                'article': news.article,
                'news_nickname': news_nickname,
                'keyword': news.keyword,
                'push_time': time_format(news.push_time),
            }
            recommend_lst.append(recommend_dic)

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