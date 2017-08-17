#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *

database = MySQLDatabase('devops', **{'host': '192.168.234.132', 'password': 'admin', 'port': 3306, 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Workflow(BaseModel):
    comment = CharField(null=True)
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