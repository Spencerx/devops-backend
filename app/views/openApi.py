#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

common = Blueprint('common',__name__)
from app.models.teams import Teams
from app.models.services import Services
from app.models.users import Users
from app.tools.jsonUtils import response_json


@common.route('/team')
def team_list():
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
    except Exception,e:
        return ''


@common.route('/service')
def service_list():
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
    except Exception,e:
        return ''

@common.route('/user')
def user_list():
    try:
        users = Users.select()
        data = []
        for user in users:
            per_user = {
                'id': user.id,
                'service_name': user.username
            }
            data.append(per_user)
        return jsonify(data)
    except Exception,e:
        return ''


@common.route('/pinyin_trans',methods=['POST', 'OPTIONS'])
def pinyin_trans():
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
