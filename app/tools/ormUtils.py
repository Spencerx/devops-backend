#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.users import Users
from app.models.teams import Teams
from app.models.services import Services
from app.models.status import Status
from app.models.flow_type import FlowType
from app.models.roles import Roles

# id和中文名的转换工具集


def id_to_team(id):
    try:
        t = Teams.select().where(Teams.t == id).get()
        return t.team_name
    except Exception, e:
        return ""


def id_to_user(id):
    try:
        u = Users.select().where(Users.id == id).get()
        return u.name
    except Exception, e:
        return ""


def id_to_service(id):
    try:
        s = Services.select().where(Services.s == id).get()
        return s.service_name
    except Exception, e:
        return ""


def id_to_status(id):
    try:
        s = Status.select().where(Status.s == id).get()
        return s.status_info
    except Exception, e:
        return ""


def id_to_flow_type(id):
    try:
        s = FlowType.select().where(FlowType.id == id).get()
        return s.type
    except Exception, e:
        return ""

def id_to_role(id):
    try:
        s = Roles.select().where(Roles.r == id).get()
        return s.role_name
    except Exception, e:
        return ""


def user_to_id(user):
    try:
        u = Users.select().where(Users.name == user).get()
        return u.id
    except Exception, e:
        return ""


def team_to_id(team):
    try:
        t = Teams.select().where(Teams.team_name == team).get()
        return t.t
    except Exception, e:
        return ""


def status_to_id(status):
    try:
        s = Status.select().where(Status.status_info == status).get()
        return s.s
    except Exception, e:
        return ""


def service_to_id(service):
    try:
        s = Services.select().where(Services.service_name == service).get()
        return s.s
    except Exception, e:
        return ""


def flow_type_to_id(flow_type):
    try:
        s = FlowType.select().where(FlowType.type == flow_type).get()
        return s.id
    except Exception, e:
        return ""


def role_to_id(role):
    try:
        s = Roles.select().where(Roles.role_name == role).get()
        return s.r
    except Exception, e:
        return ""


def querylastversion_by_id(id):
    try:
        if id:
            s = Services.select().where(Services.s == int(id)).get()
            return s.current_version
        else:
            return ""
    except Exception, e:
        return ""
