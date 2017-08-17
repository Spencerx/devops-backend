#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
import requests

#移除https警告
requests.packages.urllib3.disable_warnings()

def generate_salt_token():
    url = current_app.config['SALT_LOGIN_URL']
    headers = {'Accept':'application/json'}
    login_payload = {'username':current_app.config['SALT_USERNAME'],'password':current_app.config['SALT_PASSWORD'],'eauth':current_app.config['SALT_EAUTH']}
    try:
        login_request = requests.post(url=url,headers=headers,data=login_payload,verify=False)
        token = login_request.json()['return'][0]['token']
        return token
    except Exception,e:
        print 'salt api token except'
        return ''


def exec_commands(token,cmd):
    url = current_app.config['SALT_BASE_URL']
    headers = {'Accept': 'application/json',"X-Auth-Token":token}
    exec_playload = {'client':'local','tgt':'*','fun':'cmd.run','arg':cmd}
    exec_request = requests.post(url,headers=headers,data=exec_playload,verify=False)
    return exec_request.json()


