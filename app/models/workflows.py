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
    service = CharField(null=True)
    create_time = DateTimeField()
    deploy_info = CharField(null=True)
    dev_user = CharField()
    jenkins_version = CharField(null=True)
    last_jenkins_version = CharField(null=True)
    production_user = CharField()
    sql_info = CharField(null=True)
    team_name = CharField()
    test_user = CharField()
    v_version = CharField(null=True)
    w = PrimaryKeyField(db_column='w_id')

    class Meta:
        db_table = 'workflow'