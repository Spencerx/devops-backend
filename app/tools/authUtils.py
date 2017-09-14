#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from app.models.passport import User


def varify_passwd(username, password):
    is_exsist = User.select().where(User.username == username).count()
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
        if password == md5_password:
            return {'status': 200, 'result': True}
        else:
            return {'status': 200, 'result': False}


