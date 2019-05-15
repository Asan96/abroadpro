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
from view.transaction import transaction_load
from view.problem import problem_load
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



    # 投稿专栏
    url(r'^news/$', news_load.load_news_page, name='load_news_page'),
    url(r'^news_table_init/$', news_main.news_table_init, name='news_table_init'),
    # 编辑文章
    url(r'^edit/$', news_load.load_edit_page, name='load_edit_page'),
    url(r'^edit_news_save/$', news_main.edit_news_save, name='edit_news_save'),  # 保存草稿
    url(r'^edit_news_submit/$', news_main.edit_news_submit, name='edit_news_submit'),  # 发布文章
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
    # 注意事项
    url(r'^note/$', news_load.load_note_page, name='load_note_page'),
    # 浏览文章
    url(r'^browsing_news/$', news_load.load_browsing_page, name='browsing_news'),




    # 社交专栏
    url(r'^communicate/$', communicate_load.load_communicate_page, name='load_communicate_page'),
    # 留言板
    url(r'^communicate_table_init/$', communicate_main.communicate_table_init, name='communicate_table_init'),
    # 添加好友
    url(r'^add_friend/$', communicate_load.load_add_friend_page, name='add_friend'),
    url(r'^search_user/$', communicate_main.search_user, name='search_user'),  # 查找用户
    url(r'^add_friend_msg/$', communicate_main.add_friend_msg, name='add_friend_msg'),  # 查找用户
    # 我的好友
    url(r'^my_friend/$', communicate_load.load_my_friend_page, name='my_friend'),
    # 好友管理
    url(r'^manage_friend/$', communicate_load.load_manage_friend_page, name='manage_friend'),
    # 浏览留言
    url(r'^browsing_message/$', communicate_load.load_browsing_page, name='browsing_message'),
    url(r'^check_friend/$', communicate_main.check_friend, name='check_friend'),   # 审核好友通知




    # 交易专栏
    url(r'^transaction/$', transaction_load.load_transaction_page, name='load_transaction_page'),



    # 疑难解答
    url(r'^problem/$', problem_load.load_problem_page, name='load_problem_page'),

]
