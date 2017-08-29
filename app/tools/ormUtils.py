#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.users import Users
from app.models.teams import Teams
from app.models.services import Services
from app.models.status import Status


def id_to_team(id):
    t = Teams.select().where(Teams.t==id).get()
    return t.team_name


def id_to_user(id):
    u = Users.select().where(Users.id==id).get()
    return u.username


def id_to_service(id):
    s = Services.select().where(Services.s == id).get()
    return s.service_name


def id_to_status(id):
    s = Status.select().where(Status.s == id).get()
    return s.status_info



