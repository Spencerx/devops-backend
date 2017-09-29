#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class FlowType(BaseModel):
    id = IntegerField()
    type = CharField()

    class Meta:
        db_table = 'flow_type'
