# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:39
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from abroad.models import *
from django.contrib.auth.decorators import login_required
from abroad.views import *
from abroad.view import *


@login_required
@csrf_exempt
def load_news_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, "news/news.html", locals())

@login_required
@csrf_exempt
def load_browsing_page(request):
    my_id = request.user.id
    operations, user_id, msg_count, now_nickname = public_params(request)
    params = request.GET.dict()
    nickname = params['nickname']
    news_id = params['news_id']
    news_user_id = User.objects.filter(nickname=nickname).values_list('id', flat=True).first()
    new = News.objects.filter(user_id=news_user_id, id=news_id).first()
    comments = Comment.objects.filter(news_id=new.id).order_by('create_time')
    comments_lst = []
    for comment in comments:
        reply_lst = []
        comment_nickname = User.objects.filter(id=comment.user_id).values_list('nickname', flat=True).first()
        replies = ReplyComment.objects.filter(comment_id=comment.id)
        for reply in replies:
            reply_nickname = User.objects.filter(id=reply.user_id).values_list('nickname', flat=True).first()
            reply_dic = {
                'user_id': reply.user_id,
                'reply_id': reply.id,
                'reply_nickname': reply_nickname,
                'reply': reply.reply,
                'create_time': time_format(reply.create_time),
            }
            reply_lst.append(reply_dic)
        comments_dic = {
            'user_id': comment.user_id,
            'comment_id': comment.id,
            'comment_nickname': comment_nickname,
            'comment': comment.comment,
            'create_time': time_format(comment.create_time),
            'replys': reply_lst,
        }
        comments_lst.append(comments_dic)
    return render(request, "news/browsing_news.html", locals())

# 编辑文章
@login_required
@csrf_exempt
def load_edit_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    countrys = Location.objects.filter(level='2')
    clas = NewsKeyword.objects.filter(type='0')
    if request.user.username == 'admin':
        clas =NewsKeyword.objects.filter()
    # types = NewsKeyword.objects.filter(type='1')
    return render(request, "news/edit_news.html", locals())

# 我的推送
@login_required
@csrf_exempt
def load_push_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, "news/push_news.html", locals())


# 我的草稿
@csrf_exempt
def load_draft_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    countrys = Location.objects.filter(level='2')
    clas = NewsKeyword.objects.filter(type='0')
    return render(request, "news/draft_news.html", locals())

@csrf_exempt
def select_school_init(request):
    country = request.POST.get('country')
    school_str = ''
    schools = list(Location.objects.filter(level='3', country=country).values_list('school', flat=True))
    for school in schools:
        school += ','
        school_str += school
    return HttpResponse(json.dumps({'msg': school_str}), content_type='application/json')
