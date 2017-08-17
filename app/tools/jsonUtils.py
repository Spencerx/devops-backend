#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify

def response_json(status_code,message):
    return jsonify({'ststus':status_code,'message':message})