# -*- coding: utf-8 -*-
"""abroadpro URL Configuration

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  url(r'^$', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from view.login import login_load
from view.news import news_load
from view.communicate import communicate_load
from view.transaction import transaction_load
from view.problem import problem_load
import views

urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    # 首页
    url(r'^base/$', views.load_base_page),
    # 登陆注册
    url(r'^login/$', login_load.login_page_load),
    url(r'^login_verify/$', login_load.login_verify, name='login_verify'),
    url(r'^login_register/$', login_load.login_register, name='login_register'),
    url(r'^send_verify_msg/$', login_load.send_verify_msg, name='send_verify_msg'),
    url(r'^check_verify_msg/$', login_load.check_verify_msg, name='check_verify_msg'),
    url(r'^modify_password/$', login_load.modify_password, name='modify_password'),
    # 投稿专栏
    url(r'^news/$', news_load.load_news_page, name='load_news_page'),
    # 社交专栏
    url(r'^communicate/$', communicate_load.load_communicate_page, name='load_communicate_page'),
    # 交易专栏
    url(r'^transaction/$', transaction_load.load_transaction_page, name='load_transaction_page'),
    # 疑难解答
    url(r'^problem/$', problem_load.load_problem_page, name='load_problem_page'),

]
