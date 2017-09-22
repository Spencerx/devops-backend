#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from app.private_config import DATABASE, PASSPORT_DATABASE


def create_peewee_connection():
    database = MySQLDatabase(DATABASE['db'], **{'host': DATABASE['host'], 'password': DATABASE['passwd'],
                                                'port': DATABASE['port'], 'user': DATABASE['user']})
    return database


def create_passport_connection():
    database = MySQLDatabase(PASSPORT_DATABASE['db'], **{'host': PASSPORT_DATABASE['host'],
                                                         'password': PASSPORT_DATABASE['passwd'],
                                                         'port': PASSPORT_DATABASE['port'],
                                                         'user': PASSPORT_DATABASE['user']})
    return database
