#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from app.models.passport import User


def varify_passwd(username, password):
    """
    end服务中验证账号密码
    :param username: 登陆用户名
    :param password: 登陆密码
    :return:
    """
    is_exsist = User.select().where(User.username == username).count()
    # end服务中不存在此用户
    if is_exsist < 1:
        return {'status': 500, 'result': u'用户不存在'}
    else:
        u = User.select().where(User.username == username).get()
        md = hashlib.md5()
        salt = u.createby
        md5_password = u.password
        hybrid_password = password + '{' + str(salt) + '}'
        md.update(hybrid_password)
        password = md.hexdigest()
        # 验证成功
        if password == md5_password:
            return {'status': 200, 'result': True}
        # 账号密码不匹配
        else:
            return {'status': 200, 'result': False}


