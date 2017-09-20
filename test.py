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
import datetime
import gevent
from gevent import monkey
monkey.patch_all()


def f(n):
    for i in range(n):
        gevent.sleep(1)
        print i
start = datetime.datetime.now()
f(5)
f(3)
f(2)
end = datetime.datetime.now()
print end - start

start = datetime.datetime.now()
g1 = gevent.spawn(f,5)
g2 = gevent.spawn(f,3)
g3 = gevent.spawn(f,2)
gevent.joinall([g1, g2, g3])
end = datetime.datetime.now()
print end-start


