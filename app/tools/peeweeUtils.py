#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *


def create_peewee_connection():
    database = MySQLDatabase('devops', **{'host': '127.0.0.1', 'password': 'admin', 'port': 3306, 'user': 'root'})
    return database


def create_passport_connection():
    database = MySQLDatabase('highso_db1', **{'host': '127.0.0.1', 'password': 'admin', 'port': 3306, 'user': 'root'})
    return database
