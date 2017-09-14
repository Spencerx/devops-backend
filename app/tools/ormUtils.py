#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.users import Users
from app.models.teams import Teams
from app.models.services import Services
from app.models.status import Status

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
        return u.username
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


def user_to_id(user):
    try:
        u = Users.select().where(Users.username == user).get()
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
        s = Services.select().where(Services.service_name == int(service)).get()
        return s.id
    except Exception, e:
        return ""





