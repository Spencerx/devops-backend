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
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot(qr_path="./1.jpg")
# bot.file_helper.send('Hello World!')
# bot.self.send('Hello World!')
print bot.self.name
print bot.self.user_name
print bot.self.wxid
u = bot.user_details(bot.self.user_name)
print u.sex
bot.logout()
