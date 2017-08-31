#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, current_app
from app.tools.saltUtils import generate_salt_token,exec_commands
from app.tools.tokenUtils import generate_token, check_token_status
from app.tools.redisUtils import create_redis_connection
from app.tools.jsonUtils import response_json
from app.models.users import Users
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from xpinyin import Pinyin
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        form_data = request.get_json()
        username = form_data['username']
        password = form_data['password']
        try:
            u = Users.select().where(Users.username==username).get()
        except Exception, e:
            current_app.logger.warn(e)
            return response_json(500, u'用户不存在', data='')
        if u:
            password_hash = u.password
            if check_password_hash(password_hash,password):
                if u.is_active == '1':
                    r = create_redis_connection()
                    token = generate_token(username)
                    r.setex(username,token,24*60*60*30)
                    data = {
                        'username': username,
                        'password': u.password,
                        'role': u.role,
                        'is_active': u.is_active,
                        'token': token,
                        'uid': u.id
                    }
                    current_app.logger.info('user:{0} get token {1} success'.format(username,token))
                    return response_json(200,'',data=data)
                else:
                    return response_json(500, u'账号未激活', '')

            else:
                return response_json(500, u'密码不正确','')
    else:
        return ''


@auth.route('/logout',methods=['POST'])
def logout():
    if request.method=="POST":
        r = create_redis_connection()
        username = request.get_json()['username']
        try:
            r.delete(username)
            current_app.logger.info('user:{0} has safely logout'.format(username))
            return response_json(200, '', '')
        except Exception,e:
            return response_json(500, e, '')
    else:
        return ''


@auth.route('/register',methods=['POST'])
def register():
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']
    role = json_data['role']
    is_active = json_data['is_active']
    is_exist = Users.select().where(Users.username == username).count()
    if is_exist > 0:
        return response_json(500, 'this account has been registed', '')
    else:
        p = Pinyin()
        name_pinyin = p.get_pinyin(u"{0}".format(username), '')
        passwd_hash = generate_password_hash(password,salt_length=8)
        u = Users(username=username, password=passwd_hash, role=role, is_active=is_active, name_pinyin=name_pinyin)
        try:
            u.save()
            current_app.logger.info('user:{0} register success'.format(username))
            return response_json(200, '', passwd_hash)
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
        return ''


@auth.route('/salt_token')
def token():
    token = generate_salt_token()
    if token:
        print token
        res = exec_commands(token, 'w')
        return str(res['return'])


