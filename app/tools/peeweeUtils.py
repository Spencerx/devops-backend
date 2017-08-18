#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
def create_peewee_connection():
    database = MySQLDatabase('devops', **{'host': '192.168.234.132', 'password': 'admin', 'port': 3306, 'user': 'root'})
    return database