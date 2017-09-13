#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import Blueprint, request
from app.models.teams import Teams
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user

team = Blueprint('team', __name__)


@team.route('/create', methods=['POST', 'OPTION'])
def create():
    if request.method == "POST":
        json_data = request.get_json()
        team_name = json_data['team_name']
        team_leader = json_data['team_name']
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t = Teams(team_name=team_name, team_leader=team_leader, create_time=create_time, team_status=1)
        try:
            t.save()
            return response_json(200, "", "创建成功")
        except Exception, e:
            return response_json(500, e, "")
    else:
        return response_json(200, "", "")


@team.route('/delete', methods=['POST', 'OPTION'])
def delete():
    pass


@team.route('/modify', methods=['POST', 'OPTION'])
def modify():
    pass


@team.route('/query', methods=['GET', 'OPTION'])
def query():
    if request.method == "GET":
        try:
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


