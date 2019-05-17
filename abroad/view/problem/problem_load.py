# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:45
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from abroad.models import *
from abroad.view import *



@login_required
@csrf_exempt
def load_problem_page(request):
    operations = Operating.objects.values()
    return render(request, "problem/problem.html", locals())


@login_required
@csrf_exempt
def load_my_question_page(request):
    operations = Operating.objects.values()
    return render(request, "problem/my_question.html", locals())


@login_required
@csrf_exempt
def load_my_answer_page(request):
    operations = Operating.objects.values()
    return render(request, "problem/my_answer.html", locals())


@login_required
@csrf_exempt
def load_note_problem_page(request):
    operations = Operating.objects.values()
    return render(request, "problem/note_problem.html", locals())


@login_required
@csrf_exempt
def load_browsing_question_page(request):
    operations = Operating.objects.values()
    question_id = request.GET.get('question_id')
    question = Question.objects.filter(id=question_id).first()
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
def load_browsing_answer_page(request):
    operations = Operating.objects.values()
    return render(request, "problem/browsing_answer.html", locals())

# @csrf_exempt
# def load_browsing_answer_page(request):
