#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from app.tools.jsonUtils import response_json


config = Blueprint('config', __name__)


@config.route('/create')
def create():
    response_json(200, '', '')
