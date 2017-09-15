#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from app.tools.tokenUtils import decrypt_token, check_token_status
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_role
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


@user.route('/user', methods=["POST"])
def user_list():
    """
    获取所有用户接口 前端分页获取
    :return:
    """
    if request.method == "POST":
        form_data = request.get_json()
        per_size = form_data['size']
        page_count = form_data['page']
        if page_count == 0:
            us = Users.select().limit(10).order_by(Users.id.desc())
        else:
            us = Users.select().limit(int(per_size)).offset((int(page_count) - 1) * int(per_size)).order_by(Users.id.desc())
        data = []
        for u in us:
            per_user = {
                "uid": u.id,
                "create_time": u.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "username": u.username,
                "role": id_to_role(u.role),
                "role_code": u.role,
                "is_active": u'激活' if int(u.is_active) == 1 else u"未激活",
                "can_approved": u'有' if int(u.can_approved) == 1 else u"无",
                "email": u.email,
                "name": u.name,
            }
            data.append(per_user)
        user_count = Users.select().count()
        return response_json(200, '', {'count': user_count, "data": data})
    else:
        return response_json(200, '', '')


@user.route("/active_delete", methods=["POST"])
def active_delete():
    """
    激活 or 禁用用户 根据post过来的is_active来判断激活还是禁用 1:禁用 2:激活
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        uid = json_data['uid']
        is_active = json_data['is_active']
        try:
            if is_active == "1":
                u = Users.select().where(Users.id == int(uid)).get()
                u.is_active = "0"
                u.save()
                return response_json(200, '', u'禁用用户成功')
            elif is_active == "2":
                t = Users.select().where(Users.id == int(uid)).get()
                t.is_active = "1"
                t.save()
                return response_json(200, '', u'激活用户成功')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, "", "")



