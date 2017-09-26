#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from peewee import *

env = os.environ.get('ads_env', 'dev')
if env == 'prod':
    from ..private_config import ProdConfig as Config
else:
    from ..private_config import DevConfig as Config


def create_peewee_connection():
    database = MySQLDatabase(Config.DATABASE['db'], **{'host': Config.DATABASE['host'], 'password': Config.DATABASE['passwd'],
                                                       'port': Config.DATABASE['port'], 'user': Config.DATABASE['user']})
    return database


def create_passport_connection():
    database = MySQLDatabase(Config.PASSPORT_DATABASE['db'], **{'host': Config.PASSPORT_DATABASE['host'],
                                                                'password': Config.PASSPORT_DATABASE['passwd'],
                                                                'port': Config.PASSPORT_DATABASE['port'],
                                                                'user': Config.PASSPORT_DATABASE['user']})
    return database
