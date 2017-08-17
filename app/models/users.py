#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python -m pwiz -e mysql -H 192.168.234.132 -p3306 -uroot -P  devops > db.py


from peewee import *

database = MySQLDatabase('devops', **{'host': '192.168.234.132', 'password': 'admin', 'port': 3306, 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    password = CharField()
    username = CharField()

    class Meta:
        db_table = 'users'