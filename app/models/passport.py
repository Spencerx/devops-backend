#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from app.tools.peeweeUtils import create_passport_connection


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = create_passport_connection()


class User(BaseModel):
    createby = BigIntegerField(db_column='createBy', null=True)
    createbyname = CharField(db_column='createByName', null=True)
    createdate = DateTimeField(db_column='createDate')
    deleted = IntegerField()
    departmentid = BigIntegerField(db_column='departmentId', index=True)
    email = CharField(null=True)
    entrydate = DateTimeField(db_column='entryDate', null=True)
    id = BigIntegerField(primary_key=True)
    lastlogindate = DateTimeField(db_column='lastLoginDate', null=True)
    lastupdatepwddate = DateTimeField(db_column='lastUpdatePwdDate', null=True)
    mobilenumber = CharField(db_column='mobileNumber')
    nickname = CharField(db_column='nickName', null=True)
    password = CharField()
    personname = CharField(db_column='personName', null=True)
    rank = CharField(null=True)
    status = IntegerField()
    updateby = BigIntegerField(db_column='updateBy', null=True)
    updatedate = DateTimeField(db_column='updateDate', null=True)
    username = CharField()

    class Meta:
        db_table = 'user'



