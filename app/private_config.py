#!/usr/bin/env python
# -*- coding: utf-8 -*-


# email
MAIL_HOST = 'smtp.exmail.qq.com'
MAIL_PORT = '465'
MAIL_ACCOUNT = 'security@haixue.com'
MAIL_PASSWORD = 'Haixue20170906'

# secret_key
secret_key = "d731566a30d3a66c0edbc7036fbcba9f"


# email task redis
TASK_QUEUE = {
    'REDIS_IP': '127.0.0.1',
    'REDIS_PORT': 6379,
    'REDIS_DB': 0
}

# email confirm url prefix
EMAIL_CONFIRM_PREFIX = 'http://127.0.0.1:8888/api/v1/common/confirm'
