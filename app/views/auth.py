#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户鉴权是在end服务数据库来验证密码 但是第一次登陆即使鉴权登陆 用户是未激活状态 也要在运维系统中完成身份信息的补全
    然后系统管理员在运维系统中激活该用户。
    因为end服务数据库的用户信息不完全符合运维系统。非首次登陆运维系统 只需要在end鉴权 然后在运维系统获取
    身份信息就行
"""
import datetime
from flask import Blueprint, request, current_app
from app.tools.saltUtils import generate_salt_token,exec_commands
from app.tools.tokenUtils import generate_token, check_token_status
from app.tools.redisUtils import create_redis_connection
from app.tools.jsonUtils import response_json
from app.tools.authUtils import varify_passwd
from app.models.users import Users
# from xpinyin import Pinyin
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    """
    登陆接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        username = form_data['username']
        password = form_data['password']
        # 在end服务中验证账户密码
        res = varify_passwd(username, password)
        if res['status'] == 500:
            return response_json(500, u'用户不存在', data='')
        elif res['status'] == 200 and not res['result']:
            return response_json(500, u'密码错误', data='')
        else:
            is_register = Users.select().where(Users.username == username).count()
            # 验证通过后判断是否在运维系统中注册
            if is_register > 0:
                u = Users.select().where(Users.username == username).get()
                if int(u.is_active) == 1:
                    r = create_redis_connection()
                    token = generate_token(username)
                    r.setex(username, token, 24 * 60 * 60 * 30)
                    data = {
                        'username': username,
                        'role': u.role,
                        'is_active': u.is_active,
                        'token': token,
                        'uid': u.id,
                        'name': u.name
                    }
                    current_app.logger.info('user:{0} get token {1} success'.format(username, token))
                    return response_json(200, '', data=data)
                else:
                    return response_json(500, u'请联系管理员激活账户', data='')
            else:
                return response_json(500, u'第一次登陆需要注册后账号激活后才能登陆', data='')
    else:
        return response_json(200, '', '')


@auth.route('/logout', methods=['POST'])
def logout():
    """
    注销接口
    :return:
    """
    if request.method == "POST":
        r = create_redis_connection()
        username = request.get_json()['username']
        try:
            r.delete(username)
            current_app.logger.info('user:{0} has safely logout'.format(username))
            return response_json(200, '', '')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, '', '')


@auth.route('/register', methods=['POST'])
def register():
    """
    注册接口
    :return:
    """
    json_data = request.get_json()
    username = json_data['username']
    # Chiness Name
    name = json_data['name']
    password = json_data['password']
    role = json_data['role']
    email = json_data['email']
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    is_active = "0"
    is_exist = Users.select().where(Users.username == username).count()
    if is_exist > 0:
        return response_json(500, u'该账号已被注册', '')
    else:
        res = varify_passwd(username, password)
        if res['status'] == 500:
            return response_json(500, u'用户不存在', data='')
        elif res['status'] == 200 and not res['result']:
            return response_json(500, u'密码错误', data='')
        else:
            u = Users(username=username, role=role, is_active=is_active, create_time=create_time,
                      name_pinyin=username, email=email, name=name, can_approved="0")
            try:
                u.save()
                current_app.logger.info('user:{0} register success'.format(username))
                return response_json(200, '', '')
            except Exception, e:
                current_app.logger.info('user:{0} register faild,exception:{1}'.format(username, 1))
                return response_json(500, e, '')


@auth.route('/token_status', methods=['POST'])
def check_status():
    if request.method == "POST":
        token = request.headers.get('Authorization', None)
        username = request.get_json()['username']
        t = check_token_status(username, token)
        if t:
            return response_json(200, '', '')
        else:
            return response_json(500, '', '')
    else:
        return response_json(200, '', '')


@auth.route('/salt_token')
def token():
    token = generate_salt_token()
    if token:
        print token
        res = exec_commands(token, 'w')
        return str(res['return'])


