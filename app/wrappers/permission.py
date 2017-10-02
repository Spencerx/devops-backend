#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from urlparse import urljoin
import base64
from functools import wraps
from flask import request
from app.tools.jsonUtils import response_json
from app.models.users import Users


def manager_required(func):
    """
    重要api权限装饰器 主要用于判断当前用户是否为管理员
    :param func:
    :return:
    """
    @wraps(func)
    def check_perm(*args, **kwargs):
        json_data = request.get_json()
        uid = int(json_data['uid'])
        u = Users.select().where(Users.id == uid).get()
        if int(u.is_admin) == 1:
            return func(*args, **kwargs)
        else:
            return response_json(500, u'当前用户没有管理员权限', '')
    return check_perm
