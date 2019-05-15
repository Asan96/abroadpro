# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 18:03
# @Author  : wangluchao
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from abroad.models import *
from django.db.models import Q
from django.utils import timezone
from abroad.view import *

import json


class CommunicateManage:
    def __init__(self):
        self.type_dic = {
            'normal': '0',
            'notice': '1'
        }
        self.state_dic = {
            'unread': '0',
            'read': '1'
        }
        self.type_cn_dic = {
            '0':'留言',
            '1':'通知',
        }
        self.state_cn_dic = {
            '0': '未读',
            '1': '已读',
        }
        self.userObj = User.objects
        self.relationshipObj = Relationship.objects
        self.messageObj = Message.objects
        self.now = timezone.now()

    def search_user(self, search_word, my_id):
        user_lst = []
        users = self.userObj.filter(Q(username__icontains=search_word) | Q(nickname__icontains=search_word)).exclude(id=my_id)
        for user in users:
            friendObj = self.relationshipObj.filter(user_id=my_id, friend_id=user.id)
            user_dic = {
                'user_id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'birthday': date_format(user.birthday),
                'sex': '男' if user.sex == '1' else '女'
            }
            if friendObj:
                user_dic['operate'] = '已关注'
            else:
                user_dic['operate'] = '关注'
            user_lst.append(user_dic)
        if users:
            return users.count(), user_lst
        else:
            return 0, []

    def add_friend_msg(self, request):
        params = request.POST.dict()
        my_nickname = request.user.nickname.encode('utf-8')
        msg = my_nickname+' 想添加你为好友'
        msg_dict ={
            'from_user_id': request.user.id,
            'to_user_id': params['user_id'],
            'message': msg,
            'state': self.state_dic['unread'],
            'type': self.type_dic['notice'],
        }
        addMsgObj = self.messageObj.filter(**msg_dict)
        if addMsgObj:
            return {'ret': False, 'msg': '您已发送过申请！'}
        else:
            try:
                msg_dict['create_time'] = self.now
                self.messageObj.create(**msg_dict)
                return {'ret': True, 'msg': '好友申请发送成功！'}
            except Exception, e:
                return {'ret': False, 'msg': '申请发送失败！'+str(e)}

    def communicate_table_init(self, user_id):
        msg_lst = []
        msgs = self.messageObj.filter(to_user_id=user_id)
        for msg in msgs:
            from_user = self.userObj.filter(id=msg.from_user_id).values('nickname', 'username').first()
            msg_dic = {
                'msg_id': msg.id,
                'from_username': from_user['username'],
                'from_nickname': from_user['nickname'],
                'create_time': time_format(msg.create_time),
                'message': msg.message,
                'state': self.state_cn_dic[msg.state],
                'type': self.type_cn_dic[msg.type],
            }
            msg_lst.append(msg_dic)
        return len(msg_lst), msg_lst

    def check_friend(self, request):
        params = request.POST.dict()
        user_id = request.user.id
        check_num = int(params['check_num'])
        msg_id = params['msg_id']
        from_user_id = params['from_user_id']
        if check_num:
            relation1_dic = {
                'user_id': user_id,
                'friend_id': from_user_id,
                'create_time': self.now,
            }
            relation2_dic = {
                'user_id': from_user_id,
                'friend_id': user_id,
                'create_time': self.now,
            }
            try:
                self.relationshipObj.create(relation1_dic)
                self.relationshipObj.create(relation2_dic)
                self.messageObj.filter(id=msg_id).update(state=self.state_dic['read'])
                return {'ret': True, 'msg': '同意好友申请成功！'}
            except Exception, e:
                return {'ret': False, 'msg': '出错了！'+str(e)}
        else:
            try:
                self.messageObj.filter(id=msg_id).update(state=self.state_dic['read'])
                return {'ret': False, 'msg': '已拒绝好友申请！'}
            except Exception, e:
                return {'ret': False, 'msg': '出错了！'+str(e)}


@csrf_exempt
def search_user(request):
    params = request.POST.dict()
    search_word = params['search_word']
    limit = int(params['limit'])
    offset = int(params['offset'])
    my_id = request.user.id
    total, rows = CommunicateManage().search_user(search_word, my_id)
    row_lst = rows[offset:offset+limit]
    return HttpResponse(json.dumps({'total': total, 'rows': row_lst}))

@csrf_exempt
def add_friend_msg(request):
    result = CommunicateManage().add_friend_msg(request)
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def communicate_table_init(request):
    params = request.POST.dict()
    user_id = request.user.id
    limit = int(params['limit'])
    offset = int(params['offset'])
    total, rows=CommunicateManage().communicate_table_init(user_id)
    row_lst = rows[offset:offset+limit]
    return HttpResponse(json.dumps({'total': total, 'rows': row_lst}))


@csrf_exempt
def check_friend(request):
    result = CommunicateManage().check_friend(request)
    return HttpResponse(json.dumps(result), content_type='application/json')



