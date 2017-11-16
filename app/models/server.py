#!/usr/bin/env python
# -*- coding: utf-8 -*-


from peewee import *
from app.tools.peeweeUtils import create_peewee_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class Servers(BaseModel):
    id = PrimaryKeyField(db_column='id')
    hostname = CharField(null=True)
    internal_ip = CharField()
    outernal_ip = CharField(null=True)
    ssh_passwd = CharField()
    ssh_port = IntegerField()
    ssh_user = CharField()
    type = CharField()

    class Meta:
        db_table = 'servers'
