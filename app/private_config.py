#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config:
    def __init__(self):
        pass
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

    # email redis queue key
    EMAIL_QUEUE_KEY = "email:consume:tasks"


class DevConfig(Config):
    def __init__(self):
        pass

    # email confirm url prefix
    EMAIL_CONFIRM_PREFIX = 'http://127.0.0.1:8888/api/v1/common/confirm'

    # peewee config
    # devops数据库
    DATABASE = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'admin',
        'db': 'devops'
    }

    # end服务鉴权数据库
    PASSPORT_DATABASE = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'admin',
        'db': 'highso_db1'
    }


class ProdConfig(Config):
    def __init__(self):
        pass

    # email confirm url prefix
    EMAIL_CONFIRM_PREFIX = 'http://42.62.97.75:18888/api/v1/common/confirm'

    # peewee config
    # devops数据库
    DATABASE = {
        'host': '127.0.0.1',
        'port': 13306,
        'user': 'root',
        'passwd': 'admin',
        'db': 'devops'
    }

    # end服务鉴权数据库
    PASSPORT_DATABASE = {
        'host': '127.0.0.1',
        'port': 13306,
        'user': 'root',
        'passwd': 'admin',
        'db': 'highso_db1'
    }

