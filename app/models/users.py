#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python -m pwiz -e mysql -H 127.0.0.1 -p3306 -uroot -P  devops > db.py
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
    name_pinyin = CharField()
    can_approved = CharField()
    email = CharField()
    name = CharField()

    class Meta:
        db_table = 'users'
