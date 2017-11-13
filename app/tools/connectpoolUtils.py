#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import consul
from flask import current_app


def create_redis_connection():
    """
    从redis连接池获取连接
    :return:
    """
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'], db=0,)
    r = redis.Redis(connection_pool=pool)
    return r


def create_consul_connection():
    """
    consul 连接池
    :return:
    """
    c = consul.Consul(host=current_app.config['CONSUL_CONFIG']['host'],
                      port=current_app.config['CONSUL_CONFIG']['port'],
                      scheme=current_app.config['CONSUL_CONFIG']['scheme'])
    return c
