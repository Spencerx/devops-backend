#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from app.tools.tokenUtils import decrypt_token, check_token_status
from app.tools.jsonUtils import response_json
from app.models.users import Users
from app.models.workflows import Workflow

user = Blueprint('user', __name__)


@user.route('/userinfo', methods=['POST'])
def userinfo():
    """
    获取用户信息接口
    :return:
    """
    if request.method == 'POST':
        token = request.headers.get('Authorization', None)
        if token:
            username = decrypt_token(token)
            if not check_token_status(username=username, token=token):
                return response_json(500, u'token已经失效', '')
            if username:
                try:
                    u = Users.select().where(Users.username == username).get()
                    user_role = u.role
                    uid = u.id
                    can_approved = u.can_approved
                    my_flow_count = 0
                    if int(user_role) == 2:
                        my_flow_count += Workflow.select().where(Workflow.status == 2).count()

                    if int(user_role) == 4:
                        my_flow_count += Workflow.select().where((Workflow.status == 3) & (Workflow.test_user == uid)).count()

                    if can_approved:
                        my_flow_count += Workflow.select().where(Workflow.status == 1).count()

                    data = {
                        'username': username,
                        'role': u.role,
                        'is_active': u.is_active,
                        'myflow_count': my_flow_count,
                        'uid': u.id,
                        'token': token,
                        'name_pinyin': u.name_pinyin if u.name_pinyin else '',
                    }
                except Exception, e:
                    return response_json(500, u'用户未找到', '')
                if u:
                    return response_json(200, '', data=data)
            else:
                return response_json(500, u'token已经失效', '')
        else:
            return response_json(500, u'无效token', '')
    else:
        return ''


