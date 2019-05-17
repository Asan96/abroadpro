# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:39
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *
from django.contrib.auth.decorators import login_required
from abroad.views import page_init


@login_required
@csrf_exempt
def load_news_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "news/news.html", locals())

@login_required
@csrf_exempt
def load_browsing_page(request):
    operations, now_nickname = page_init(request)
    params = request.GET.dict()
    nickname = params['nickname']
    title = params['title']
    user_id = User.objects.filter(nickname=nickname).values_list('id', flat=True).first()
    new = News.objects.filter(user_id=user_id, title=title).first()
    return render(request, "news/browsing_news.html", locals())

# 编辑文章
@login_required
@csrf_exempt
def load_edit_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "news/edit_news.html", locals())

# 我的推送
@login_required
@csrf_exempt
def load_push_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "news/push_news.html", locals())

# 注意事项
@csrf_exempt
def load_note_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "news/note_news.html", locals())

# 我的草稿
@csrf_exempt
def load_draft_page(request):
    operations, now_nickname = page_init(request)
    return render(request, "news/draft_news.html", locals())