#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify

common = Blueprint('common',__name__)
from app.models.teams import Teams
from app.models.services import Services
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