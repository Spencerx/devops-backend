#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.tools.peeweeUtils import create_peewee_connection
from peewee import *


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()


class Users(BaseModel):
    id = CharField()
    username = CharField()
    role = CharField()
    is_active = CharField()
    is_admin = CharField()
    name_pinyin = CharField()
    can_approved = CharField()
    email = CharField()
    name = CharField()
    create_time = DateTimeField()

    class Meta:
        db_table = 'users'
