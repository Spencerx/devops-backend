#!/usr/bin/env python
# -*- coding: utf-8 -*-


#import datetime
#a = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#print type(a)
#
#from xpinyin import Pinyin
#
#p = Pinyin()
#
#print p.get_pinyin(u'孙麒麟','')
#
#from app.models.users import Users
#
#u = Users.select()
#for i in u:
#    if i.can_approved:
#     print i.can_approved
# 导入模块

users = [
    {'name': 'a', 'age': 1},
    {'name': 'b', 'age': 2},
    {'name': 'c', 'age': 3},
]

print [[i['name'], i['age']] for i in users]
