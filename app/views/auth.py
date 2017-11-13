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
from app.tools.connectpoolUtils import create_redis_connection
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
        remember_me = form_data['remember']

        # 预先判断账户是否为锁定用户
        r = create_redis_connection()
        limit_login_key = 'login_retry_limit_{0}'.format(username)  # redis lock key
        current_limit_count = r.get('login_retry_limit_{0}'.format(username))  # lock count
        if current_limit_count == "3":
            return response_json(500, u'该账户多次登陆验证失败,已被锁定 剩余等待时长: {0} s'.format(r.ttl(limit_login_key)), data='')

        # 在end服务中验证账户密码
        res = varify_passwd(username, password)
        if res['status'] == 500:
            current_app.logger.warn('user {0} not exsist'.format(username))
            return response_json(500, u'用户不存在', data='')
        elif res['status'] == 200 and not res['result']:
            """redis 验证记录失败登陆次数 超过三次 该账号锁定1小时"""
            if current_limit_count == "2":
                current_app.logger.warn('user {0} has been locked'.format(username))
                r.setex(limit_login_key, "3", 60 * 60 * 1)
                return response_json(500, u'账户被锁定一小时,请联系运维', data='')
            else:
                r.incr(limit_login_key)
                return response_json(500, u'密码错误', data='')

        else:
            is_register = Users.select().where(Users.username == username).count()
            # 验证通过后判断是否在运维系统中注册
            if is_register > 0:
                u = Users.select().where(Users.username == username).get()
                if int(u.is_active) == 1:
                    # 删除登陆密码错误次数限制
                    r.delete(limit_login_key)
                    token_in_redis = r.get(username)
                    # 通过redis是否存在token来判断是否重新生成token 实现同一个账户多端登陆 如果每次都生成token会导致多客户端登陆挤掉上次的客户端
                    if token_in_redis:
                        data = {
                            'username': username,
                            'role': u.role,
                            'is_active': u.is_active,
                            'token': token_in_redis,
                            'uid': u.id,
                            'name': u.name
                        }
                        current_app.logger.info('user {0} get token in redis success'.format(username))
                        return response_json(200, '', data=data)
                    new_token = generate_token(username)
                    # 登陆页面点击记住密码token缓存10天 否则缓存24小时
                    r.setex(username, new_token, 24 * 60 * 60 * 10) if remember_me \
                        else r.setex(username, new_token, 24 * 60 * 60 * 1)
                    data = {
                        'username': username,
                        'role': u.role,
                        'is_active': u.is_active,
                        'token': new_token,
                        'uid': u.id,
                        'name': u.name
                    }
                    current_app.logger.info('user {0} generate new token {1} success'.format(username, new_token))
                    from app import sse
                    sse.publish({"message": "{0} now login! welcome".format(username)}, type='greeting')
                    return response_json(200, '', data=data)
                else:
                    current_app.logger.warn('user {0} try to login but account is not actived'.
                                            format(username))
                    return response_json(500, u'请联系管理员激活账户', data='')
            else:
                current_app.logger.warn('user {0} try to login but account is not registed'.
                                        format(username))
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
            current_app.logger.info('user {0} has safely logout'.format(username))
            from app import sse
            sse.publish({"message": "{0} now logout!".format(username)}, type='greeting')
            return response_json(200, '', '')
        except Exception, e:
            current_app.logger.error('redis delete token of user {0} failed, message:{1}'.format(username, e.message))
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
    # 中文名
    name = str(json_data['name']).strip()
    password = str(json_data['password']).strip()
    role = json_data['role']
    email = str(json_data['email']).strip()
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    is_active = "0"
    is_exist = Users.select().where(Users.username == username).count()
    if is_exist > 0:
        current_app.logger.warn('user {0} has been registed'.format(username))
        return response_json(500, u'该账号已被注册', '')
    else:
        res = varify_passwd(username, password)
        if res['status'] == 500:
            current_app.logger.warn('user {0} try to regist but account is not exsist'.format(username))
            return response_json(500, u'用户不存在', data='')
        elif res['status'] == 200 and not res['result']:
            current_app.logger.info('user {0} try to regist but password is wrong'.format(username))
            return response_json(500, u'密码错误', data='')
        else:
            u = Users(username=username, role=role, is_active=is_active, create_time=create_time,
                      name_pinyin=username, email=email, name=name, can_approved="0", is_admin="0")
            try:
                u.save()
                current_app.logger.info('user {0} register success'.format(username))
                return response_json(200, '', '')
            except Exception, e:
                current_app.logger.error('user {0} register faild,message:{1}'.format(username, e.message))
                return response_json(500, e, '')


@auth.route('/token_status', methods=['POST'])
def check_status():
    """
    前端的路由钩子验证token接口
    :return:
    """
    if request.method == "POST":
        token_in_header = request.headers.get('Authorization', None)
        username = request.get_json()['username']
        try:
            t = check_token_status(username, token_in_header)
        except Exception, e:
            current_app.logger.error("api passport in redis has error,message:{0}".format(e.message))
            return response_json(500, e.message, '')
        if t:
            return response_json(200, '', '')
        else:
            return response_json(500, '', '')
    else:
        return response_json(200, '', '')


@auth.route('/salt_token')
def token():
    """
    获取saltstatck token接口
    todo
    :return:
    """
    salt_token = generate_salt_token()
    if salt_token:
        print salt_token
        res = exec_commands(salt_token, 'w')
        return str(res['return'])
