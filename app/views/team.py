#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import Blueprint, request
from app.models.teams import Teams
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user, user_to_id

team = Blueprint('team', __name__)


@team.route('/create', methods=['POST', 'OPTION'])
def create():
    """
    新建团队
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        team_name = json_data['team_name']
        team_leader = user_to_id(json_data['team_leader'])
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t = Teams(team_name=team_name, team_leader=team_leader, create_time=create_time, team_status=1)
        try:
            t.save()
            return response_json(200, "", "创建成功")
        except Exception, e:
            return response_json(500, e, "")
    else:
        return response_json(200, "", "")


@team.route('/active_delete', methods=['POST', 'OPTION'])
def active_delete():
    """
    激活or禁用团队 is_active参数来判断具体操作: 1:禁用 2:激活
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        t_id = json_data['t_id']
        is_active = json_data['is_active']
        try:
            if is_active == "1":
                t = Teams.select().where(Teams.t == int(t_id)).get()
                t.team_status = 2
                t.save()
                return response_json(200, '', u'禁用团队成功')
            elif is_active == "2":
                t = Teams.select().where(Teams.t == int(t_id)).get()
                t.team_status = 1
                t.save()
                return response_json(200, '', u'激活团队成功')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, "", "")


@team.route('/modify', methods=['POST', 'OPTION'])
def modify():
    """
    修改团队
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        t_id = json_data['t_id']
        new_team_name = json_data['team_name']
        new_team_leader = user_to_id(json_data['team_leader'])
        try:
            t = Teams.select().where(Teams.t == int(t_id)).get()
            t.team_name = new_team_name
            t.team_leader = new_team_leader
            t.save()
            return response_json(200, '', u'修改成功')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, "", "")


@team.route('/query', methods=['GET', 'OPTION'])
def query():
    """
    查询团队 is_filter_disactived来判断是否返回未激活的团队
    :return:
    """
    if request.method == "GET":
        try:
            if request.args.get("is_filter_disactived",None):
                teams = Teams.select().where(Teams.team_status == 1)
            else:
                teams = Teams.select()
            data = []
            for team in teams:
                per_team = {
                    'id': team.t,
                    'team_name': team.team_name,
                    'create_time': team.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                    'team_leader': id_to_user(team.team_leader),
                    "team_sum": 10,
                    'team_status': u'激活' if int(team.team_status) == 1 else u"未激活",
                }
                data.append(per_team)
            return response_json(200, "", data=data)
        except Exception, e:
            return response_json(500, e, "")
    else:
        return response_json(200, "", "")


