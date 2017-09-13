#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class Teams(BaseModel):
    t = PrimaryKeyField(db_column='t_id')
    team_name = CharField()
    team_leader = CharField()
    team_status = CharField()
    create_time = DateTimeField()


    class Meta:
        db_table = 'teams'
