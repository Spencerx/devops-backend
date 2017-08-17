#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, current_app
from app.tools.saltUtils import generate_salt_token,exec_commands
from app.tools.tokenUtils import generate_token, decrypt_token
from app.tools.redisUtils import create_redis_connection
from app.tools.jsonUtils import response_json
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app.models.users import Users


auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        u = Users.select().where(Users.username==username).get()
    except Exception,e:
        current_app.logger.warn(e)
        return response_json(500,'user is not exist')
    if u:
        password_hash = u.password
        if check_password_hash(password_hash,password):
            r = create_redis_connection()
            token = generate_token(username)
            r.setex(username,token,24*60*60*30)
            current_app.logger.info('user:{0} get token {1} success'.format(username,token))
            return response_json(200,token)
        else:
            return response_json(500, 'password is not correct')


@auth.route('/logout',methods=['POST'])
def logout():
    r = create_redis_connection()
    username = request.form['username']
    r.delete(username)
    current_app.logger.info('user:{0} has safely logout'.format(username))
    return username

@auth.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    is_exist = Users.select().where(Users.username==username).count()
    if is_exist>0:
        return response_json(500,'this account has been registed')
    else:
        passwd_hash = generate_password_hash(password,salt_length=8)
        u = Users(username=username,password=passwd_hash)
        try:
            u.save()
            current_app.logger.info('user:{0} register success'.format(username))
            return response_json(200,passwd_hash)
        except Exception,e:
            current_app.logger.info('user:{0} register faild,exception:{1}'.format(username,1))
            return response_json(500,e)


@auth.route('/salt_token')
def token():
    token = generate_salt_token()
    if token:
        print token
        res = exec_commands(token,'w')
        return str(res['return'])

@auth.route('/userinfo',methods=['POST'])
def userinfo():
    token = request.form['token']
    username = decrypt_token(token)
    return username

