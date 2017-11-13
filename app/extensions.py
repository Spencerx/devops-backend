#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""flask 避免循环导入"""
from flask_apscheduler import APScheduler
from apscheduler.schedulers.gevent import GeventScheduler

"""注意 此处虽然加了文件锁限制apscheduler的个数为1 但是此处多worker 依旧会创建多个实例子 但只有一个实例被参数化了
       在view模块引用 会引用不了加载了配置的aps的实例
       所以gunicorn 启动参数需要添加 --preload
    The --preload flag tells Gunicorn to "load the app before forking the worker processes".
"""


"""经验证 上述不成立"""
gevent_sched = GeventScheduler()
scheduler = APScheduler(scheduler=gevent_sched)
print '===== init scheduler ===='
print scheduler
