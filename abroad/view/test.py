# -*- coding: utf-8 -*-
import os, django,random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abroadpro.settings")
django.setup()

from abroad.models import *
from abroad.view import MyEmail


def test():
    # MyEmail(
    #     to_list=['1158529652@qq.com'],
    #     tag='test',
    #     content={
    #         'content': '车阿萨德发色的发',
    #         'type': 'plain',
    #         'coding': 'utf-8'
    #     }
    # ).send()
    while True:
        verify_msg = str(random.randint(100000, 999999))
        print verify_msg

if __name__=='__main__':
    test()
