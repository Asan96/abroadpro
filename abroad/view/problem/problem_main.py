# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 18:41
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from abroad.models import *
from django.utils import timezone
from abroad.view import *

import json


class ProblemManage(object):
    def __init__(self):
        self.questionObj = Question.objects
        self.answerObj = Answer.objects
        self.userObj = User.objects
        self.question_state_dic = {
            'unAnswer': '0',
            'answer': '1'
        }
        self.is_best_dic = {
            'notBest': '0',
            'best': '1'
        }
        self.question_cn_state_dic = {
            '0': '未解答',
            '1': '已解答'
        }
        self.is_best_cn_dic = {
            '0' : '否',
            '1' : '是'
        }
        self.now = timezone.now()

    def raise_question(self, user_id, question):
        question = question.strip()
        if not question:
            return {'ret': False, 'msg': '问题内容不得为空！'}
        question_dic = {
            'user_id': user_id,
            'question': question,
            'state': self.question_state_dic['unAnswer'],
            'create_time': self.now
        }
        try:
            self.questionObj.create(**question_dic)
            return {'ret': True, 'msg': '提问成功！'}
        except Exception, e:
            return {'ret': False, 'msg': '出错了！'+str(e)}

    def my_question_table_init(self, user_id):
        question_lst = []
        questions = self.questionObj.filter(user_id=user_id)
        for question in questions:
            question_dic = {
                'question_id': question.id,
                'question': question.question,
                'state': question.state,
                'create_time': time_format(question.create_time),
            }
            question_lst.append(question_dic)
        return len(question_lst), question_lst

    def my_question_child_table_init(self, question_id):
        answer_lst = []
        answers = self.answerObj.filter(question_id=question_id)
        for answer in answers:
            user = self.userObj.filter(id=answer.user_id).first()
            answer_dic = {
                'answer_id': answer.id,
                'question_id': question_id,
                'nickname': user.nickname,
                'like_num': answer.like_num,
                'create_time': time_format(answer.create_time),
                'is_best': self.is_best_cn_dic[answer.is_best],
                'answer': answer.answer,
            }
            answer_lst.append(answer_dic)
        return len(answer_lst), answer_lst

    def delete_question(self, question_id):
        try:
            self.answerObj.filter(question_id=question_id).delete()
            self.questionObj.filter(id=question_id).delete()
            return {'ret': True, 'msg': '删除成功！'}
        except Exception, e:
            return {'ret': False, 'msg': '出错了！' + str(e)}

    def question_table_init(self, user_id, params):
        question_lst = []
        limit = params['limit']
        offset = params['offset']
        sort = params.get('sort', '')
        order = params.get('sortOrder', '')
        questionObj = self.questionObj.exclude(user_id=user_id)
        if sort:
            if order == 'asc':
                questionObj = questionObj.order_by(sort)
            else:
                questionObj = questionObj.order_by('-'+sort)
        total = questionObj.count()
        questions = questionObj.values()[offset:limit+offset]
        for question in questions:
            user = self.userObj.filter(id=question['user_id']).first()
            question_dic = {
                'question_id': question['id'],
                'nickname': user.nickname,
                'question': question['question'],
                'state': self.question_cn_state_dic[question['state']],
                'create_time': time_format(question['create_time'])
            }
            question_lst.append(question_dic)
        return total, question_lst

    def answer_question(self, user_id, question_id, answer):
        answer = answer.strip()
        if not answer:
            return {'ret': False, 'msg': '回答内容不得为空！'}
        elif len(answer) >= 400:
            return {'ret': False, 'msg': '回答内容不得超过四百字！'}
        answerExist = self.answerObj.filter(question_id=question_id, user_id=user_id)
        if answerExist:
            return {'ret': False, 'msg': '您已回答过该问题！'}
        answer_dict = {
            'question_id': question_id,
            'user_id': user_id,
            'like_num': 0,
            'create_time': self.now,
            'is_best': self.is_best_dic['notBest'],
            'answer': answer,
        }
        self.answerObj.create(**answer_dict)
        return {'ret': True, 'msg': '回答成功！'}
# 提出问题
@csrf_exempt
def raise_question(request):
    user_id = request.user.id
    question = request.POST.get('question')
    result = ProblemManage().raise_question(user_id, question)
    return HttpResponse(json.dumps(result), content_type='application/json')

# 我的问题表
@csrf_exempt
def my_question_table_init(request):
    params = request.POST.dict()
    limit = int(params['limit'])
    offset = int(params['offset'])
    user_id = request.user.id
    total, rows = ProblemManage().my_question_table_init(user_id)
    rows_lst = rows[offset:limit+offset]
    return HttpResponse(json.dumps({'total': total, 'rows': rows_lst}))


# 问题子表: 回答表
@csrf_exempt
def my_question_child_table_init(request):
    question_id = request.POST.get('question_id')
    total, rows = ProblemManage().my_question_child_table_init(question_id)
    return HttpResponse(json.dumps({'total': total, 'rows': rows}))


# 删除问题
@csrf_exempt
def delete_question(request):
    question_id = request.POST.get('question_id')
    result = ProblemManage().delete_question(question_id)
    return HttpResponse(json.dumps(result), content_type='application/json')


# 问题列表
@csrf_exempt
def question_table_init(request):
    params = request.POST.dict()
    user_id = request.user.id
    total, rows = ProblemManage().question_table_init(user_id, params)
    return HttpResponse(json.dumps({'total': total, 'rows': rows}))


# 回答问题
@csrf_exempt
def answer_question(request):
    params = request.POST.dict()
    answer = params['answer']
    question_id = params['question_id']
    user_id = request.user.id
    result = ProblemManage().answer_question(user_id, question_id, answer)
    return HttpResponse(json.dumps(result), content_type='application/json')







