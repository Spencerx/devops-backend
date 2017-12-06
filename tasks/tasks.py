#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yagmail
from datetime import datetime
from celery import Celery
import os


env = os.environ.get('ads_env', 'dev')
if env == 'prod':
    from config import Prod as Config
else:
    from config import Dev as Config

"""all task dispatch"""
celery = Celery('tasks')
celery.conf.update(
    BROKER_URL=Config.BROKER_URL,
    BROKER_POOL_LIMIT=2,
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_BACKEND=Config.CELERY_RESULT_BACKEND,
)


@celery.task()
def week_report():
    """
    运维周报task 上周一周上线统计
    :return:
    """
    print 'task start ...'
    print datetime.now()
    yag = yagmail.SMTP('security@haixue.com', 'Haixue20170906', host='smtp.exmail.qq.com', port=465)
    yag.send(to='591356683@qq.com',
             subject='test',
             contents='hello,world')
    return 'task demo finish'

