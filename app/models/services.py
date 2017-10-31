#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class Services(BaseModel):
    s = PrimaryKeyField(db_column='s_id')
    service_name = CharField()
    comment = CharField()
    type = CharField(null=True)
    language = CharField(null=True)
    service_status = CharField()
    service_leader = IntegerField()
    deploy_script = IntegerField()
    create_time = DateTimeField()
    current_version = CharField(null=True)
    is_switch_flow = IntegerField(default=2)

    class Meta:
        db_table = 'services'
