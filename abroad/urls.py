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
from view.news import news_load, news_main
from view.communicate import communicate_load, communicate_main
from view.problem import problem_load, problem_main
from view.manage import manage
import views

urlpatterns = [
    # 模板继承页
    url(r'^base/$', views.load_base_page),
    # 首页
    url(r'^home/$', views.load_home_page),
    # 登陆注册
    url(r'^login/$', login_load.login_page_load),
    url(r'^login_verify/$', login_load.login_verify, name='login_verify'),
    url(r'^login_register/$', login_load.login_register, name='login_register'),
    url(r'^send_verify_msg/$', login_load.send_verify_msg, name='send_verify_msg'),
    url(r'^check_verify_msg/$', login_load.check_verify_msg, name='check_verify_msg'),
    url(r'^modify_password/$', login_load.modify_password, name='modify_password'),


    # 登出
    url(r'^log_out/$', views.log_out, name='log_out'),

    # 注意事项
    url(r'^note/$', views.load_note_page, name='load_note_page'),

    # 投稿专栏
    url(r'^news/$', news_load.load_news_page, name='load_news_page'),
    url(r'^news_table_init/$', news_main.news_table_init, name='news_table_init'),
    # 编辑文章
    url(r'^edit/$', news_load.load_edit_page, name='load_edit_page'),
    url(r'^edit_news_save/$', news_main.edit_news_save, name='edit_news_save'),  # 保存草稿
    url(r'^edit_news_submit/$', news_main.edit_news_submit, name='edit_news_submit'),  # 发布文章
    url(r'^select_school_init/$', news_load.select_school_init, name='select_school_init'),  # 学校加载
    # 我的草稿
    url(r'^draft/$', news_load.load_draft_page, name='load_draft_page'),
    url(r'^draft_table_init/$', news_main.my_draft, name='draft_table_init'),
    url(r'^delete_my_draft/$', news_main.delete_my_draft, name='delete_my_draft'),
    url(r'^load_original_draft/$', news_main.load_original_draft, name='load_original_draft'),  # 加载原草稿
    url(r'^draft_modify_save/$', news_main.draft_modify_save, name='draft_modify_save'),  # 保存草稿修改
    url(r'^draft_submit/$', news_main.draft_submit, name='draft_submit'),  # 草稿推送
    # 我的推送
    url(r'^push/$', news_load.load_push_page, name='load_push_page'),
    url(r'^push_table_init/$', news_main.my_push, name='push_table_init'),
    url(r'^delete_my_push/$', news_main.delete_my_push, name='delete_my_push'),
    # 浏览文章
    url(r'^browsing_news/$', news_load.load_browsing_page, name='browsing_news'),
    url(r'^comment/$', news_main.comment, name='comment'),  # 评论
    url(r'^reply_comment/$', news_main.reply_comment, name='reply_comment'),  # 回复评论
    url(r'^delete_comment/$', news_main.delete_comment, name='delete_comment'),  # 删除评论
    url(r'^delete_reply/$', news_main.delete_reply, name='delete_reply'),  # 删除回复




    # 社交专栏
    url(r'^communicate/$', communicate_load.load_communicate_page, name='load_communicate_page'),
    # 留言板
    url(r'^communicate_table_init/$', communicate_main.communicate_table_init, name='communicate_table_init'),
    url(r'^delete_message/$', communicate_main.delete_message, name='delete_message'),  # 删除留言
    # 添加好友
    url(r'^add_friend/$', communicate_load.load_add_friend_page, name='add_friend'),
    url(r'^search_user/$', communicate_main.search_user, name='search_user'),  # 查找用户
    url(r'^add_friend_msg/$', communicate_main.add_friend_msg, name='add_friend_msg'),  # 查找用户
    # 我的好友
    url(r'^my_friend/$', communicate_load.load_my_friend_page, name='my_friend'),
    url(r'^my_friend_table_init/$', communicate_main.my_friend_table_init, name='my_friend_table_init'),  # 我的好友表
    url(r'^send_message/$', communicate_main.send_message, name='send_message'),  # 发送留言
    url(r'^delete_friend/$', communicate_main.delete_friend, name='delete_friend'),  # 删除好友
    # 浏览留言
    url(r'^browsing_message/$', communicate_load.load_browsing_page, name='browsing_message'),
    url(r'^check_friend/$', communicate_main.check_friend, name='check_friend'),   # 审核好友通知
    url(r'^read_message/$', communicate_main.read_message, name='read_message'),   # 读留言




    # 问答专栏
    url(r'^problem/$', problem_load.load_problem_page, name='load_problem_page'),
    url(r'^question_table_init/$', problem_main.question_table_init, name='question_table_init'),
    url(r'^answer_question/$', problem_main.answer_question, name='answer_question'),
    url(r'^answer_like/$', problem_main.answer_like, name='answer_like'),
    # 我的问题
    url(r'^my_question/$', problem_load.load_my_question_page, name='my_question'),
    url(r'^raise_question/$', problem_main.raise_question, name='raise_question'),  # 提出问题
    url(r'^my_question_table_init/$', problem_main.my_question_table_init, name='my_question_table_init'),  # 我的问题表
    url(r'^my_question_child_table_init/$', problem_main.my_question_child_table_init, name='my_question_child_table_init'),  # 问题子表
    url(r'^delete_question/$', problem_main.delete_question, name='delete_question'),  # 删除问题
    # 我的回答
    url(r'^my_answer/$', problem_load.load_my_answer_page, name='my_answer'),
    url(r'^delete_answer/$', problem_main.delete_answer, name='delete_answer'),
    # 浏览问题
    url(r'^browsing_question/$', problem_load.load_browsing_question_page, name='browsing_question'),
    url(r'^browsing_question_answer_like/$', problem_main.browsing_question_answer_like, name='browsing_question_answer_like'),  # 浏览问题点赞
    # 提出问题
    url(r'^raise_question_page/$', problem_load.load_raise_question_page, name='raise_question_page'),


    # 超级管理员
    # 管理文章
    url(r'^manage_news/$', manage.load_manage_news_page, name='manage_news'),

]
