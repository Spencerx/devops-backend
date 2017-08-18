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
    war_url = CharField(null=True)

    class Meta:
        db_table = 'services'