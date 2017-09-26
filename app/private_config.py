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

    # email redis queue key
    EMAIL_QUEUE_KEY = "email:consume:tasks"


class DevConfig(Config):
    def __init__(self):
        pass

    # email task redis
    TASK_QUEUE = {
        'REDIS_IP': '127.0.0.1',
        'REDIS_PORT': 6379,
        'REDIS_DB': 0
    }

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

    # email task redis
    TASK_QUEUE = {
        'REDIS_IP': '127.0.0.1',
        'REDIS_PORT': 16379,
        'REDIS_DB': 0
    }

    # email confirm url prefix
    EMAIL_CONFIRM_PREFIX = 'http://deploy.highso.com.cn/api/v1/common/confirm'

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
        'host': '192.168.1.54',
        'port': 3306,
        'user': 'masterdb0',
        'passwd': 'Mastertech!@#20170918',
        'db': 'highso_db1'
    }

