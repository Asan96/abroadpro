# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:45
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from abroad.models import *
from abroad.view import *
from abroad.views import *



@login_required
@csrf_exempt
def load_problem_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    categorys = QuestionCategory.objects.filter()
    # questions = Question.objects.filter()
    # question_lst = []
    # for question in questions:
    #     answer_lst = []
    #     question_nickname = User.objects.filter(id=question.user_id).values_list('nickname', flat=True).first()
    #     category = QuestionCategory.objects.filter(id=question.category_id).values_list('category', flat=True).first()
    #     answers = Answer.objects.filter(question_id=question.id)
    #     for answer in answers:
    #         like_user_id_lst = LikeAnswer.objects.filter(answer_id=answer.id).values_list('user_id', flat=True)
    #         like_nickname_lst = User.objects.filter(id__in=like_user_id_lst).values_list('nickname', flat=True)
    #         answer_nickname = User.objects.filter(id=answer.user_id).values_list('nickname', flat=True).first()
    #         answer_dic = {
    #             'answer_id': answer.id,
    #             'answer_nickname': answer_nickname,
    #             'like_num': answer.like_num,
    #             'answer_time': time_format(answer.create_time),
    #             'answer': answer.answer,
    #             'like_lst': str(like_nickname_lst),
    #         }
    #         answer_lst.append(answer_dic)
    #     question_dic = {
    #         'question_nickname': question_nickname,
    #         'title': question.title,
    #         'question': question.question,
    #         'state': '未解答' if question.state == '0' else '已解答',
    #         'question_time': time_format(question.create_time),
    #         'categroy': category,
    #         'answer_num': question.answer_num,
    #         'answer': answer_lst,
    #     }
    #     question_lst.append(question_dic)

    return render(request, "problem/problem.html", locals())


@login_required
@csrf_exempt
def load_my_question_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    return render(request, "problem/my_question.html", locals())


@login_required
@csrf_exempt
def load_my_answer_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    user_id = request.user.id
    answers = Answer.objects.filter(user_id=user_id)
    empty_lst = []
    my_answer_lst = []
    for answer in answers:
        other_answer_lst = []
        question = Question.objects.filter(id=answer.question_id).values().first()
        question_nickname = User.objects.filter(id=question['user_id']).values_list('nickname',flat=True).first()
        answer_dic = {
            'question_nickname': question_nickname,
            'answer_id': answer.id,
            'question_id': answer.question_id,
            'question': question['question'],
            'question_title': question['title'],
            'category': QuestionCategory.objects.filter(id=question['category_id']).values_list('category', flat=True).first(),
            'create_time': time_format(answer.create_time),
            'answer': answer.answer,
            'like_num': answer.like_num,
        }
        my_answer_lst.append(answer_dic)
    my_answer_count = len(my_answer_lst)
    return render(request, "problem/my_answer.html", locals())


@login_required
@csrf_exempt
def load_browsing_question_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    question_id = request.GET.get('question_id')
    question = Question.objects.filter(id=question_id).first()
    category = QuestionCategory.objects.filter(id=question.category_id).values_list('category', flat=True).first()
    question_create_time = time_format(question.create_time)
    question_nickname = User.objects.filter(id=question.user_id).values_list('nickname', flat=True).first()
    answers = Answer.objects.filter(question_id=question_id).order_by('-like_num')
    answer_lst = []
    user_id = request.user.id
    for answer in answers:
        answer_nickname = User.objects.filter(id=answer.user_id).values_list('nickname', flat=True).first()
        isLikeExist = LikeAnswer.objects.filter(user_id=user_id, answer_id=answer.id)
        is_like = '1' if isLikeExist else '0'
        answer_dic = {
            'id': answer.id,
            'nickname': answer_nickname,
            'create_time': time_format(answer.create_time),
            'like_num': answer.like_num,
            'answer': answer.answer,
            'is_like': is_like
        }
        answer_lst.append(answer_dic)
    return render(request, "problem/browsing_question.html", locals())


@login_required
@csrf_exempt
def load_raise_question_page(request):
    operations, user_id, msg_count, now_nickname = public_params(request)
    categories = QuestionCategory.objects.values()
    return render(request, "problem/raise_question.html", locals())


