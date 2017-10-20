#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class ServiceBackend(BaseModel):
    """
    service to server mid table
    """
    comment = CharField(null=True)
    port = IntegerField(null=True)
    server = IntegerField(db_column='server_id', index=True, null=True)
    service = IntegerField(db_column='service_id', index=True, null=True)
    weight = IntegerField()

    class Meta:
        db_table = 'service_backend'
