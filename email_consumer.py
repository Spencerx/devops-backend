#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
异步执行邮件模块
作为消费者读取redis key为"email:consume:tasks"的列表,然后消费key
部署单独运行此进程 一般先启动此进程 再启动系统主程序
如果邮件功能故障 排查email_consumer日志
"""
import os
import redis
import logging
import sys
from app.tools.emailUtils import async_send_approved_email
from app.tools.redisUtils import create_redis_connection

env = os.environ.get('ads_env', 'dev')
if env == 'prod':
    from app.private_config import ProdConfig as Config
else:
    from app.private_config import DevConfig as Config

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='logs/email_consumer.log',
                    filemode='a+')


def create_redis_connection():
    pool = redis.ConnectionPool(host=Config.TASK_QUEUE['REDIS_IP'], port=Config.TASK_QUEUE['REDIS_PORT'], db=Config.TASK_QUEUE['REDIS_DB'])
    r = redis.Redis(connection_pool=pool)
    return r


def consume_email():
    try:
        r = create_redis_connection()
        task = r.brpop(Config.EMAIL_QUEUE_KEY, 0)
    except Exception, e:
        logging.error("email task queue redis has error message:{0}".format(e))  # redis exception
    else:
        try:
            task = eval(task[1])
            to_list = task['to_list']
            title = task['title']
            subject = task['subject']
            data = task['data']
            e_type = task['e_type']
            print task
        except Exception, e:
            logging.error("email args may has exceptions,message: {0}".format(e.message))  # args exception
        else:
            logging.info("to:{0} subject:{1}".format(str(to_list), subject))
            async_send_approved_email(to_list, subject, data, int(e_type), title=title)


if __name__ == '__main__':
    while True:
        consume_email()
