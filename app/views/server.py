#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

server = Blueprint('server', __name__)


@server.route('/server')
def server_list():
    pass
