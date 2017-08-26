#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from config import Config
from jinja2.utils import import_string
import os, logging
from flask_cors import CORS

blueprints = [
    ('app.views.auth:auth', '/api/v1/auth'),
    ('app.views.workFlow:workflow', '/api/v1/workflow'),
    ('app.views.openApi:common', '/api/v1/common'),
    ('app.views.user:user', '/api/v1/user'),
]

def create_app():
    app = Flask(__name__)
    load_config(app)
    register_blueprints(app)
    load_ext(app)
    CORS(app)
    return app


def load_config(app):
    env = os.environ.get('zen_env', 'dev')
    app.config.from_object(
        'config.Prod') if env == 'prod' else app.config.from_object('config.Dev')

    # app.debug = True
    # #接口日志
    # handler = logging.FileHandler('{0}/devops.log'.format(Config.LOG_DIR))
    # app.logger.addHandler(handler)


def load_ext(app):
    # from .extensions import db
    # from .extensions import login_manager
    # from .extensions import cas
    # from .extensions import api
    # api.init_app(app)
    # db.init_app(app)
    # api.init_app(app)
    # login_manager.session_protection = 'strong'
    # login_manager.login_view='auth.login'
    # login_manager.init_app(app)
    pass

def register_blueprints(app):
    for bp_info in blueprints:
        bp = import_string(bp_info[0])
        app.register_blueprint(bp, url_prefix=bp_info[1])

