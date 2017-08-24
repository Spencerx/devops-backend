#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from app.tools.tokenUtils import decrypt_token, check_token_status
from app.tools.jsonUtils import response_json
from app.models.users import Users

user = Blueprint('user',__name__)

@user.route('/userinfo',methods=['POST'])
def userinfo():
    if request.method == 'POST':
        token = request.get_json()['token']
        if token:
            username = decrypt_token(token)
            if not check_token_status(username=username,token=token):
                return response_json(500, u'token已经失效', '')
            if username:
                try:
                    u = Users.select().where(Users.username==username).get()
                    data = {
                        'username':username,
                        'password':u.password,
                        'role':u.role,
                        'is_active':u.is_active
                    }
                except Exception,e:
                    return response_json(500,u'用户未找到','')
                if u:
                    return response_json(200, '', data=data)
            else:
                return response_json(500, u'token已经失效', '')
        else:
            return response_json(500, u'无效token', '')
    else:
        return ''
