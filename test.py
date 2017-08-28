#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
a = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print type(a)

from xpinyin import Pinyin

p = Pinyin()

print p.get_pinyin(u'孙麒麟','')