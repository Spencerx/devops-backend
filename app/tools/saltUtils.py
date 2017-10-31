#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
import requests
from app.tools.redisUtils import create_redis_connection

# 移除https警告
requests.packages.urllib3.disable_warnings()


def generate_salt_token():
    """
    获取saltstack token,redis缓存一份 避免频繁请求salt-api
    :return:
    """
    r = create_redis_connection()
    token_in_redis = r.get("salt_token")
    if token_in_redis:
        return token_in_redis
    else:
        url = current_app.config['SALT_LOGIN_URL']
        headers = {'Accept': 'application/json'}
        login_payload = {'username': current_app.config['SALT_USERNAME'],
                         'password': current_app.config['SALT_PASSWORD'],
                         'eauth': current_app.config['SALT_EAUTH']}
        try:
            login_request = requests.post(url=url, headers=headers, data=login_payload, verify=False, timeout=30)
            token = login_request.json()['return'][0]['token']
            r.setex("salt_token", token, 1*60*60)  # redis cache 8 hours
            return token
        except Exception, e:
            current_app.logger.error(e)
            return ''


def exec_commands(host, token, cmd):
    """
    salt执行命令范例
    :param token:
    :param host:
    :param cmd:
    :return:
    """
    url = current_app.config['SALT_BASE_URL']
    headers = {'Accept': 'application/json', "X-Auth-Token": token}
    exec_playload = {'client': 'local', 'tgt': host, 'fun': 'cmd.run', 'arg': cmd, 'full_return': True}
    exec_request = requests.post(url, headers=headers, data=exec_playload, verify=False)
    return exec_request.json()


def ping_check(host, token):
    """
    salt check ping result
    :param token:
    :param host:
    :return:
    """
    url = current_app.config['SALT_BASE_URL']
    headers = {'Accept': 'application/json', "X-Auth-Token": token}
    exec_playload = {'client': 'local', 'tgt': host, 'fun': 'test.ping', 'full_return': True}
    exec_request = requests.post(url, headers=headers, data=exec_playload, verify=False, timeout=10)
    return exec_request.json()


def trans_file(host, token, file_name):
    """
    salt push file to minion
    :param token:
    :param host:
    :param file_name:
    :return:
    """
    url = current_app.config['SALT_BASE_URL']
    headers = {'Accept': 'application/json', "X-Auth-Token": token}
    exec_playload = {'client': 'local', 'tgt': host, 'fun': 'cp.get_file', "arg": ["salt://"+file_name,
                                                                                   "/opt/"+file_name],
                     'full_return': True}
    exec_request = requests.post(url, headers=headers, data=exec_playload, verify=False, timeout=30)
    return exec_request.json()


