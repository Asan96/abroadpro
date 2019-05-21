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
from django.db.models import Q

import json


class ProblemManage(object):
    def __init__(self):
        self.questionObj = Question.objects
        self.answerObj = Answer.objects
        self.userObj = User.objects
        self.likeObj = LikeAnswer.objects
        self.categoryObj = QuestionCategory.objects
        self.question_state_dic = {
            'unAnswer': '0',
            'answer': '1'
        }
        self.question_cn_state_dic = {
            '0': '未解答',
            '1': '已解答'
        }
        self.now = timezone.now()

    def raise_question(self, params, user_id):
        question = params['question'].strip()
        category_id = params['category_id']
        title = params['title'].strip()
        if not title:
            return {'ret': False, 'msg': '问题描述不得为空！'}
        if not category_id:
            return {'ret': False, 'msg': '问题分类不得为空！'}
        question_dic = {
            'user_id': user_id,
            'title': title,
            'question': question,
            'state': self.question_state_dic['unAnswer'],
            'create_time': self.now,
            'category_id': category_id,
            'answer_num': 0,
        }
        try:
            self.questionObj.create(**question_dic)
            return {'ret': True, 'msg': '提问成功！'}
        except Exception, e:
            return {'ret': False, 'msg': '出错了！'+str(e)}

    def my_question_table_init(self, user_id, limit, offset):
        question_lst = []
        total = self.questionObj.filter(user_id=user_id).count()
        questions = self.questionObj.filter(user_id=user_id)[offset:limit+offset]
        for question in questions:
            question_dic = {
                'question_id': question.id,
                'question': question.question,
                'title': question.title,
                'state': question.state,
                'category': self.categoryObj.filter(id=question.category_id).values_list('category', flat=True).first(),
                'create_time': time_format(question.create_time),
                'answer_num': question.answer_num,
            }
            question_lst.append(question_dic)
        return total, question_lst

    def my_question_child_table_init(self, question_id, user_id, params):
        answer_lst = []
        sort = params.get('sort', '')
        order = params.get('sortOrder', '')
        answers = self.answerObj.filter(question_id=question_id)
        if sort and order:
            if order == 'desc':
                answers = answers.order_by('-'+sort)
            else:
                answers = answers.order_by(sort)
        for answer in answers:
            user_is_like = '0'
            isLikeObj = self.likeObj.filter(answer_id=answer.id, user_id=user_id)
            if isLikeObj:
                user_is_like = '1'
            user = self.userObj.filter(id=answer.user_id).first()
            answer_dic = {
                'answer_id': answer.id,
                'question_id': question_id,
                'nickname': user.nickname,
                'like_num': answer.like_num,
                'create_time': time_format(answer.create_time),
                'answer': answer.answer,
                'user_is_like': user_is_like,
            }
            answer_lst.append(answer_dic)
        return len(answer_lst), answer_lst

    def delete_question(self, question_id):
        try:
            answer_id_lst = self.answerObj.filter(question_id=question_id).values('id')
            self.likeObj.filter(answer_id__in=answer_id_lst).delete()
            self.answerObj.filter(question_id=question_id).delete()
            self.questionObj.filter(id=question_id).delete()
            return {'ret': True, 'msg': '删除成功！'}
        except Exception, e:
            return {'ret': False, 'msg': '出错了！' + str(e)}

    def question_table_init(self, user_id, params):
        question_lst = []
        limit = params['limit']
        offset = params['offset']
        search_word = params['search_word']
        category_id = params['category_id']
        sort = params.get('sort', '')
        order = params.get('sortOrder', '')
        questionObj = self.questionObj
        if category_id:
            questionObj = questionObj.filter(category_id=category_id)
        if search_word:
            questionObj = questionObj.filter(Q(question__icontains=search_word) | Q(title__icontains=search_word))
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
                'title': question['title'],
                'nickname': user.nickname,
                'question': question['question'],
                'state': self.question_cn_state_dic[question['state']],
                'category': self.categoryObj.filter(id=question['category_id']).values_list('category', flat=True).first(),
                'create_time': time_format(question['create_time']),
                'answer_num': question['answer_num']
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
            'answer': answer,
        }
        answer_num = self.questionObj.filter(id=question_id).values_list('answer_num', flat=True).first()
        self.questionObj.filter(id=question_id).update(state=self.question_state_dic['answer'], answer_num=answer_num+1)
        self.answerObj.create(**answer_dict)
        return {'ret': True, 'msg': '回答成功！'}

    def answer_like(self, user_id, answer_id):
        like_dic = {
            'user_id': user_id,
            'answer_id': answer_id,
        }
        answerObj = self.answerObj.filter(id=answer_id)
        num = answerObj.first().like_num
        likeExistObj = self.likeObj.filter(**like_dic)
        if likeExistObj:
            likeExistObj.delete()
            num -= 1
            result = {'ret': True, 'msg': '取消点赞成功！'}
        else:
            self.likeObj.create(**like_dic)
            num += 1
            result = {'ret': True, 'msg': '点赞成功！'}
        answerObj.update(like_num=num)
        return result

    def browsing_question_answer_like(self, user_id, answer_id, is_like):
        like_dic = {
            'user_id': user_id,
            'answer_id': answer_id,
        }
        likeExist = self.likeObj.filter(**like_dic)
        answer = self.answerObj.filter(id=answer_id)
        num = answer.first().like_num
        if is_like == '1':
            if not likeExist:
                self.likeObj.create(**like_dic)
                num += 1
                answer.update(like_num=num)
                return {'ret': True, 'msg': '点赞成功'}
            else:
                return {'ret': False, 'msg': '操作过快，请稍后'}
        else:
            if likeExist:
                likeExist.delete()
                num -= 1
                answer.update(like_num=num)
                return {'ret': True, 'msg': '取消点赞成功'}
            else:
                return {'ret': False, 'msg': '操作过快，请稍后'}

    def delete_answer(self, user_id, answer_id):
        answerExist = self.answerObj.filter(user_id=user_id, id=answer_id)
        if answerExist:
            question_id = answerExist.first().question_id
            try:
                self.likeObj.filter(answer_id=answer_id).delete()
                answerExist.delete()
                answer_num = self.questionObj.filter(id=question_id).values_list('answer_num', flat=True).first()
                self.questionObj.filter(id=question_id).update(answer_num=answer_num-1)
                has_answer = self.answerObj.filter(question_id=question_id)
                if not has_answer:
                    self.questionObj.filter(id=question_id).update(state=self.question_state_dic['unAnswer'])
                return {'ret': True, 'msg': '删除成功！'}
            except Exception, e:
                return {'ret': False, 'msg': '出错了！' + str(e)}
        else:
            return {'ret': False, 'msg': '未找到该条回答！'}


# 提出问题
@csrf_exempt
def raise_question(request):
    user_id = request.user.id
    params = request.POST.dict()
    result = ProblemManage().raise_question(params, user_id)
    return HttpResponse(json.dumps(result), content_type='application/json')


# 我的问题表
@csrf_exempt
def my_question_table_init(request):
    params = request.POST.dict()
    limit = int(params['limit'])
    offset = int(params['offset'])
    user_id = request.user.id
    total, rows = ProblemManage().my_question_table_init(user_id, limit, offset)
    return HttpResponse(json.dumps({'total': total, 'rows': rows}))


# 问题子表: 回答表
@csrf_exempt
def my_question_child_table_init(request):
    user_id = request.user.id
    params = request.POST.dict()
    question_id = request.POST.get('question_id')
    total, rows = ProblemManage().my_question_child_table_init(question_id, user_id, params)
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


# 点赞回答
@csrf_exempt
def answer_like(request):
    user_id = request.user.id
    answer_id = request.POST.get('answer_id')
    result = ProblemManage().answer_like(user_id, answer_id)
    return HttpResponse(json.dumps(result), content_type='application/json')


# browsing点赞
@csrf_exempt
def browsing_question_answer_like(request):
    user_id = request.user.id
    params = request.POST.dict()
    answer_id = params['answer_id']
    is_like = params['is_like']
    result = ProblemManage().browsing_question_answer_like(user_id, answer_id, is_like)
    return HttpResponse(json.dumps(result), content_type='application/json')


# 我的回答 删除回答
@csrf_exempt
def delete_answer(request):
    user_id = request.user.id
    answer_id = request.POST.get('answer_id')
    result = ProblemManage().delete_answer(user_id, answer_id)
    return HttpResponse(json.dumps(result), content_type='application/json')
