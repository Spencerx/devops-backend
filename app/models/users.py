#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python -m pwiz -e mysql -H 192.168.234.132 -p3306 -uroot -P  devops > db.py
from app.tools.peeweeUtils import create_peewee_connection

from peewee import *

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = create_peewee_connection()

class Users(BaseModel):
    password = CharField()
    username = CharField()
    role = CharField()
    is_active = CharField()

    class Meta:
        db_table = 'users'