#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class Scripts(BaseModel):
    id = PrimaryKeyField(db_column='id')
    script_content = TextField(null=True)
    script_name = CharField(null=True)
    comment = CharField(null=True)
    type = CharField(null=True)

    class Meta:
        db_table = 'scripts'
