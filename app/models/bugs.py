#!/usr/bin/env python
# -*- coding: utf-8 -*-


from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class Bugs(BaseModel):
    id = PrimaryKeyField(db_column='id')
    flow_id = IntegerField(db_column='flow_id')
    exception_info = CharField(db_column='exception_info')

    class Meta:
        db_table = 'bugs'
