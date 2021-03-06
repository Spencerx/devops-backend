#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import base64
from pyDes import triple_des, CBC, PAD_PKCS5
from connectpoolUtils import create_redis_connection
from config import Config


secret_key = Config.SECRET_KEY


def check_token_status(username, token):
    """
    验证token的工具
    :param username:
    :param token:
    :return:
    """
    r = create_redis_connection()
    res = r.get(username)
    if res and res == token:
        return True
    else:
        return False


def generate_token(username):
    """
    token生成工具
    :param username:
    :return:
    """
    time_stamp = str(time.time())
    k = triple_des(secret_key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(str(username)+'$$$$'+time_stamp)
    return base64.b64encode(d)


def decrypt_token(token):
    """
    解密token工具
    :param token:
    :return:
    """
    k = triple_des(secret_key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    try:
        token = base64.b64decode(token)
        username = k.decrypt(token).split('$$$$')[0]
    except Exception, e:
        username = ''
    return username
