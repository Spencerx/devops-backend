#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redisUtils import create_redis_connection
import time
import base64
from pyDes import triple_des,CBC,PAD_PKCS5
from config import Config


secret_key = Config.SECRET_KEY
def check_token_status(username,token):
    r = create_redis_connection()
    res = r.get(username)
    if res and res==token:
        return True
    else:
        return False

def generate_token(username):
    time_stamp = str(time.time())
    k = triple_des(secret_key, CBC, "\0\0\0\0\0\0\0\0", pad=None,padmode=PAD_PKCS5)
    d = k.encrypt(str(username)+'$$$$'+time_stamp)
    return base64.b64encode(d)

def decrypt_token(token):
    k = triple_des(secret_key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    try:
        token = base64.b64decode(token)
        username = k.decrypt(token).split('$$$$')[0]
    except Exception,e:
        username = ''
    return username
