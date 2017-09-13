#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
openapi中的接口不需要鉴权 主要提供给外部系统访问
"""
import paramiko
import sys
from flask import Blueprint, jsonify, request, current_app
from app.models.teams import Teams
from app.models.services import Services
from app.models.users import Users
from app.tools.jsonUtils import response_json

common = Blueprint('common',__name__)
reload(sys)
sys.setdefaultencoding('utf-8')


@common.route('/team')
def team_list():
    """
    获取所有团队接口
    :return:
    """
    try:
        teams = Teams.select()
        data = []
        for team in teams:
            per_team = {
                'id': team.t,
                'team_name': team.team_name
            }
            data.append(per_team)
        return jsonify(data)
    except Exception, e:
        return ''


@common.route('/service')
def service_list():
    """
    获取所有服务接口
    :return:
    """
    try:
        services = Services.select()
        data = []
        for service in services:
            per_service = {
                'id': service.s,
                'service_name': service.service_name
            }
            data.append(per_service)
        return jsonify(data)
    except Exception, e:
        return ''


@common.route('/user')
def user_list():
    """
    获取所有注册用户接口
    :return:
    """
    try:
        users = Users.select()
        data = []
        for user in users:
            per_user = {
                'id': user.id,
                'username': user.username
            }
            data.append(per_user)
        return response_json(200, '', data=data)
    except Exception, e:
        return ''


@common.route('/dev')
def dev_list():
    """
    获取所有开发角色用户接口
    :return:
    """
    try:
        users = Users.select().where(Users.role == 3)
        data = []
        for user in users:
            per_user = {
                'id': user.id,
                'username': user.username
            }
            data.append(per_user)
        return jsonify(data)
    except Exception, e:
        return ''


@common.route('/pinyin_trans',methods=['POST', 'OPTIONS'])
def pinyin_trans():
    """
    用户名的拼音转用户名 exp:sunqilin=>孙麒麟
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        pinyin = json_data['pinyin']
        try:
            user = Users.select().where(Users.name_pinyin == pinyin).get()
            if user:
                return response_json(200, '', user.username)
            else:
                return response_json(500, 'not find', '')
        except Exception, e:
            return response_json(500, u'我好像故障了', '')
    else:
        return ""


@common.route('/check_sql', methods=['POST', 'OPTIONS'])
def check_sql():
    """
    SQLAdvisor索引优化接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        sql = json_data['sql']
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname='192.168.16.25', username='root', password='HX20170816!@#QAZcd')
        advisor_host = current_app.config['SQLADVISOR_DB']['host']
        advisor_port = current_app.config['SQLADVISOR_DB']['port']
        advisor_user = current_app.config['SQLADVISOR_DB']['user']
        advisor_password = current_app.config['SQLADVISOR_DB']['password']
        advisor_database = "highso"
        command = """/bin/sqladvisor -h {0}  -P {1}  -u {2} -p '{3}' -d {4} -q "{5}" -v 1""".format(
            advisor_host, advisor_port, advisor_user, advisor_password, advisor_database, sql)
        stdin, stdout, stderr = s.exec_command(command=command, get_pty=True)
        o = ""
        for line in stdout:
            if u"索引优化建议" in line:
                o = o + "<font color='green'>" + line + "</font>" + "<br>"
            else:
                o = o + line + "<br>"
        return response_json(200, "", o)
    else:
        return ""
