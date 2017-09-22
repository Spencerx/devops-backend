#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import logging
import sys
from app.tools.commonUtils import async_send_email
from app.tools.redisUtils import create_redis_connection
from app.private_config import TASK_QUEUE
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='../../logs/email_consumer.log',
                    filemode='a+')


def create_redis_connection():
    pool = redis.ConnectionPool(host=TASK_QUEUE['REDIS_IP'], port=TASK_QUEUE['REDIS_PORT'], db=TASK_QUEUE['REDIS_DB'])
    r = redis.Redis(connection_pool=pool)
    return r


def consume_email():
    try:
        r = create_redis_connection()
        task = r.brpop('email:consume:tasks', 0)
    except Exception, e:
        logging.error("email task queue redis has error message:".format(e.message))
    else:
        task = eval(task[1])
        to_list = task['to_list']
        subject = task['subject']
        data = task['data']
        e_type = task['e_type']
        logging.info("to:{0} subject:{1}".format(str(to_list), subject))
        async_send_email(to_list, subject, data, e_type)


while True:
    consume_email()
