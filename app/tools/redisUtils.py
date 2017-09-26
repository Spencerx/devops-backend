#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from flask import current_app


def create_redis_connection():
    """
    从redis连接池获取连接
    :return:
    """
    pool = redis.ConnectionPool(host=current_app.config['REDIS_URL'], port=current_app.config['REDIS_PORT'], db=0,)
    r = redis.Redis(connection_pool=pool)
    return r
