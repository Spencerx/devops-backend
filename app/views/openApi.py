#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
openapi中的接口不需要鉴权 主要提供给外部系统访问
"""
import paramiko
import sys
from flask import Blueprint, jsonify, request, current_app, abort
from app.models.teams import Teams
from app.models.workflows import Workflow
from app.models.services import Services
from app.models.users import Users
from app.models.roles import Roles
from app.tools.jsonUtils import response_json
from app.tools.emailUtils import decrypt_email_token

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
        current_app.logger.error("open api get all team has error message:{0}".format(e.message))
        return response_json(500, e.message, '')


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
        current_app.logger.error("open api get all service has error message:{0}".format(e))
        return response_json(500, e.message, '')


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
                'username': user.username,
                'name': user.name
            }
            data.append(per_user)
        return response_json(200, '', data=data)
    except Exception, e:
        current_app.logger.error("open api get all registed users has error message:{0}".format(e))
        return response_json(500, e.message, '')


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
        current_app.logger.error("open api get all develop users has error message:{0}".format(e.message))
        return response_json(500, e.message, '')


@common.route('/pinyin_trans', methods=['POST', 'OPTIONS'])
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
            current_app.logger.error("open api translate Chiness to pinyin has error message:{0}".format(e.message))
            return response_json(500, e.message, '')
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
        s.connect(hostname=current_app.config['SQLADVISOR_EXEC_HOST']['host'],
                  username=current_app.config['SQLADVISOR_EXEC_HOST']['user'],
                  password=current_app.config['SQLADVISOR_EXEC_HOST']['password'],
                  port=current_app.config['SQLADVISOR_EXEC_HOST']['port'])
        advisor_host = current_app.config['SQLADVISOR_DB']['host']
        advisor_port = current_app.config['SQLADVISOR_DB']['port']
        advisor_user = current_app.config['SQLADVISOR_DB']['user']
        advisor_password = current_app.config['SQLADVISOR_DB']['password']
        advisor_database = "highso_db1"
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


@common.route('/role')
def roles_list():
    """
    获取所有类型角色接口
    :return:
    """
    try:
        roles = Roles.select()
        data = []
        for role in roles:
            per_role = {
                'id': role.r,
                'role_name': role.role_name
            }
            data.append(per_role)
        return response_json(200, '', data)
    except Exception, e:
        current_app.logger.error("open api get all roles has error message:{0}".format(e.message))
        return response_json(500, e.message, '')


@common.route('/confirm')
def confirm():
    """
    邮件一键完成审批接口
    :return:
    """
    token = request.args.get('token')
    if token:
        data = decrypt_email_token(token)
        if data:
            uid = int(data['uid'])
            # 这里的工作流id可能不止一直 设计到多个flow的同时审批
            wids = str(data['w_id']).strip().split(" ")
            data = []
            for wid in wids:
                try:
                    w = Workflow.select().where(Workflow.w == int(wid)).get()
                except Exception, e:
                    current_app.logger.warn("open api of approve checked flow has been deleted message:{0}".
                                            format(e.message))
                    data.append({"id": wid, "result": u'审批过程中检测到工作流已被删除'})
                    continue
                if int(w.status) != 1:
                    current_app.logger.warn("open api of approve checked flow has been changed")
                    data.append({"id": wid, "result": u'审批过程中检测到工作流状态已改变'})
                else:
                    w.status = int(w.status) + 1
                    w.access_info = u'邮件一键快速审批'
                    w.approved_user = uid
                    w.save()
                    current_app.logger.info("one key approve flow {0} success".format(str(wid)))
                    data.append({'id': wid, "result": u'审批成功'})
            html_header = u"<table><tr><th>工作流ID</th><th>快速审批结果</th></tr>"
            html_footer = u"</table>"
            html_body = ""
            for res in data:
                row = "<font color=\"green\">{0}</font>".format(res['result']) if u"成功" in res['result']\
                            else "<font color=\"red\">{0}</font>".format(res['result'])

                html_body = html_body + "<tr><td>" + res['id'] + "</td>" + \
                                        "<td>" + row + "</td></tr>"
            html = html_header + html_body + html_footer
            return html
        else:
            current_app.logger.warn("one key approve api check token {0} is invalidate ".format(token))
            abort(403, u'非法的token')
    else:
        current_app.logger.warn("one key approve api check token is null ")
        abort(404, u'没有token')

