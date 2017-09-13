#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import timedelta


class Config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILES_DIR = os.path.join(BASE_DIR, 'files')
    UPLOAD_DIR = os.path.join(FILES_DIR, 'uploads')
    DOWNLOAD_DIR = os.path.join(FILES_DIR, 'downloads')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    SECRET_KEY = '5as7**%sd5^s7x)!'
    REMEMBER_COOKIE_DURATION = timedelta(
        seconds=3600 * 8)  # set session timeout time
    WTF_CSRF_CHECK_DEFAULT = False
    # SECRET_KEY = os.urandom(32)


class Dev(Config):
    DEBUG = True
    secret_key = '5as7**%sd5^s7x)!'
    DATABASE = {
        'host': '192.168.132.229',
        'port': 3306,
        'user': 'docker',
        'passwd': 'docker',
        'db': 'blog'
    }
    SQLADVISOR_DB = {
        'host': '42.62.97.87',
        'port': 3306,
        'user': 'techdb1',
        'password': 'techdb1#@!812!',
    }

    # salt api
    SALT_BASE_URL = 'https://192.168.234.132:8000'
    SALT_LOGIN_URL = 'https://192.168.234.132:8000/login'
    SALT_USERNAME = 'saltapi'
    SALT_PASSWORD = 'admin'
    SALT_EAUTH = 'pam'

    # redis
    REDIS_URL = '127.0.0.1'
    REDIS_PORT = 6379


class Prod(Config):
    pass
