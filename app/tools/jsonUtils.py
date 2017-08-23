#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify

def response_json(code,message,data):
    #前后端交互的api对接规范
    return jsonify({'status':code,'message':message,'data':data})