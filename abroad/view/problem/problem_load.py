# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 9:45
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from abroad.models import *


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
