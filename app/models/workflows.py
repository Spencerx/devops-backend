#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()

class Workflow(BaseModel):
    comment = CharField(null=True)
    create_time = DateTimeField()
    close_time = DateTimeField()
    current_version = CharField()
    deploy_info = CharField(null=True)
    dev_user = CharField()
    last_version = CharField(null=True)
    ops_user = IntegerField()
    production_user = CharField()
    service = CharField()
    sql_info = CharField(null=True)
    status = IntegerField()
    team_name = CharField()
    test_user = CharField()
    w = PrimaryKeyField(db_column='w_id')
    approved_user = CharField()
    class Meta:
        db_table = 'workflow'