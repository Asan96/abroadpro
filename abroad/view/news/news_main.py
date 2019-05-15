# -*- coding: utf-8 -*-
# @Time    : 2019/5/10 13:29
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from abroad.models import *
from django.utils import timezone
from abroad.view import time_format

import json


class EditNews:
    def __init__(self):
        self.newsObj = News.objects
        self.userObj = User.objects
        self.state_dict = {
            'push': '1',
            'save': '0',
        }
        self.now = timezone.now()

    def news_save(self, user_id, params,  state_key):
        title = params['title']
        keyword = params['keyword']
        article = params['article']
        existObj = self.newsObj.filter(title=title)
        state = self.state_dict[state_key]
        if existObj:
            return {'ret': False, 'msg': '文章标题已存在'}
        elif state == '0':
            self.newsObj.create(user_id=user_id, title=title, keyword=keyword, article=article, state=state,
                                create_time=self.now, update_time=self.now)
            return {'ret': True, 'msg': '文章保存成功'}
        elif state == '1':
            self.newsObj.create(user_id=user_id, title=title, keyword=keyword, article=article, state=state,
                                create_time=self.now, update_time=self.now, push_time=self.now)
            return {'ret': True, 'msg': '文章发布成功'}

    def my_article(self, user_id, state_key):
        info_lst = []
        state = self.state_dict[state_key]
        news = self.newsObj.filter(user_id=user_id, state=state)
        for new in news:
            new_info_dic = {
                'id': new.id,
                'title': new.title,
                'keyword': new.keyword,
                'article': new.article,
                'create_time': time_format(new.create_time),
                'update_time': time_format(new.update_time),
                'push_time': time_format(new.push_time),
            }
            info_lst.append(new_info_dic)
        return len(info_lst), info_lst

    def delete_article(self, news_id):
        try:
            self.newsObj.filter(id=news_id).delete()
            return {'ret': True, 'msg': '删除成功！'}
        except Exception, e:
            return {'ret': False, 'msg': '删除失败！'+str(e)}

    def news_table_init(self, title, nickname, keyword):
        news_lst = []
        search_dict = {
            'state': self.state_dict['push']
        }
        if title:
            search_dict['title'] = title
        if nickname:
            user_id = self.userObj.filter(nickname=nickname).values_list('id', flat=True).first()
            search_dict['user_id'] = user_id
        if keyword:
            search_dict['keyword'] = keyword
        news = self.newsObj.filter(**search_dict)
        for new in news:
            nickname = self.userObj.filter(id=new.user_id).values_list('nickname', flat=True).first()
            new_info_dic = {
                'id': new.id,
                'nickname': nickname,
                'title': new.title,
                'keyword': new.keyword,
                'article': new.article,
                'push_time': time_format(new.push_time),
            }
            news_lst.append(new_info_dic)
        return len(news_lst), news_lst

    def draft_load(self, news_id):
        new = self.newsObj.filter(id=news_id).first()
        new_dic = {
            'id': new.id,
            'title': new.title,
            'keyword': new.keyword,
            'article': new.article
        }
        return new_dic
    def draft_save(self, params):
        news_id = params['news_id']
        news_dic = {
            'title': params['title'],
            'keyword': params['keyword'],
            'article': params['article'],
            'update_time': self.now,
        }
        existObj = self.newsObj.filter(title=news_dic['title']).exclude(id=news_id)
        if not news_dic['title']:
            return {'ret': False, 'msg': '标题不得为空！'}
        elif existObj:
            return {'ret': False, 'msg': '标题已重复！'}
        elif not news_dic['keyword']:
            return {'ret': False, 'msg': '关键词不得为空！'}
        elif not news_dic['article']:
            return {'ret': False, 'msg': '内容不得为空！'}
        else:
            try:
                self.newsObj.filter(id=news_id).update(**news_dic)
                return {'ret': True, 'msg': '草稿保存成功！'}
            except Exception, e:
                return {'ret': False, 'msg': '保存失败！'+str(e)}

    def draft_submit(self, news_id):
        try:
            self.newsObj.filter(id=news_id).update(state=self.state_dict['push'], push_time=self.now)
            return {'ret': True, 'msg': '发布成功！'}
        except Exception, e:
            return {'ret': False, 'msg': '发布失败！'+str(e)}

# 保存草稿
@csrf_exempt
def edit_news_save(request):
    params = request.POST.dict()
    user_id = request.user.id
    result = EditNews().news_save(user_id, params, 'save')
    return HttpResponse(json.dumps(result), content_type='application/json')

# 发布文章
@csrf_exempt
def edit_news_submit(request):
    params = request.POST.dict()
    user_id = request.user.id
    result = EditNews().news_save(user_id, params, 'push')
    return HttpResponse(json.dumps(result), content_type='application/json')

# 我的推送
@csrf_exempt
def my_push(request):
    params = request.POST.dict()
    limit = int(params['limit'])
    offset = int(params['offset'])
    user_id = request.user.id
    total, rows = EditNews().my_article(user_id, 'push')
    row_lst = rows[offset:offset+limit]
    return HttpResponse(json.dumps({'total': total, 'rows': row_lst}))

# 删除推送
@csrf_exempt
def delete_my_push(request):
    params = request.POST.dict()
    news_id = params['news_id']
    result = EditNews().delete_article(news_id)
    return HttpResponse(json.dumps(result), content_type='application/json')

# 我的草稿
@csrf_exempt
def my_draft(request):
    params = request.POST.dict()
    limit = int(params['limit'])
    offset = int(params['offset'])
    user_id = request.user.id
    total, rows = EditNews().my_article(user_id, 'save')
    row_lst = rows[offset:offset+limit]
    return HttpResponse(json.dumps({'total': total, 'rows': row_lst}))

# 删除草稿
@csrf_exempt
def delete_my_draft(request):
    params = request.POST.dict()
    news_id = params['news_id']
    result = EditNews().delete_article(news_id)
    return HttpResponse(json.dumps(result), content_type='application/json')

# 文章浏览列表
@csrf_exempt
def news_table_init(request):
    params = request.POST.dict()
    limit = int(params['limit'])
    offset = int(params['offset'])
    title = params.get('title_search', '')
    nickname = params.get('nickname_search', '')
    keyword = params.get('keyword_search', '')
    total, rows = EditNews().news_table_init(title, nickname, keyword)
    row_lst = rows[offset:offset+limit]
    return HttpResponse(json.dumps({'total': total, 'rows': row_lst}))

# 原草稿加载
@csrf_exempt
def load_original_draft(request):
    news_id = request.POST.get('news_id')
    new_dic = EditNews().draft_load(news_id)
    return HttpResponse(json.dumps(new_dic), content_type='application/json')

# 保存草稿修改
@csrf_exempt
def draft_modify_save(request):
    params = request.POST.dict()
    result = EditNews().draft_save(params)
    return HttpResponse(json.dumps(result), content_type='application/json')

# 草稿发布
@csrf_exempt
def draft_submit(request):
    news_id = request.POST.get('news_id')
    result = EditNews().draft_submit(news_id)
    return HttpResponse(json.dumps(result), content_type='application/json')
