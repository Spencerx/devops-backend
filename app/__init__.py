#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from jinja2.utils import import_string
import os
import logging
from config import Config
from flask_cors import CORS
from flask_sse import sse

blueprints = [
    ('app.views.auth:auth', '/api/v1/auth'),
    ('app.views.workFlow:workflow', '/api/v1/workflow'),
    ('app.views.openApi:common', '/api/v1/common'),
    ('app.views.user:user', '/api/v1/user'),
    ('app.views.team:team', '/api/v1/team'),
    ('app.views.config:config', '/api/v1/config'),
    ('app.views.notice:notice', '/api/v1/notice'),
    ('app.views.service:service', '/api/v1/service'),
    ('app.views.elk:elk', '/api/v1/elk'),
    ('app.views.server:server', '/api/v1/server'),
    ('app.views.deploy:deploy', '/api/v1/deploy'),
    ('app.views.script:script', '/api/v1/script'),
    ('app.views.dispatch:dispatch', '/api/v1/dispatch'),
]


def create_app():
    app = Flask(__name__)
    load_config(app)
    register_blueprints(app)
    CORS(app)
    single_scheduler(app)
    app.register_blueprint(sse, url_prefix='/stream')
    return app


def load_config(app):
    env = os.environ.get('ads_env', 'dev')
    app.config.from_object(
        'config.Prod') if env == 'prod' else app.config.from_object('config.Dev')
    app.debug = True
    # 接口日志
    handler = logging.FileHandler('{0}/devops.log'.format(Config.LOG_DIR))
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)


def register_blueprints(app):
    """
    tips: 批量注册蓝图
    :param app:
    :return:
    """
    for bp_info in blueprints:
        bp = import_string(bp_info[0])
        app.register_blueprint(bp, url_prefix=bp_info[1])


def single_scheduler(app):
    """
    gunicorn multi worker 模式导致apscheduler的任务执行次数与work 数量相同
    利用文件锁 控制scheduler的启动数量
    :param app:
    :return:
    """
    import atexit
    import fcntl
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        from .extensions import scheduler
        scheduler.init_app(app)
        scheduler.start()
        print "apscheduler start success ..."
    except Exception, e:
        print e.message

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        print " release scheduler lock success ..."
        f.close()

    atexit.register(unlock)

