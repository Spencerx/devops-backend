#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify


def response_json(code, message, data):
    """
    前后端交互的api对接规范
    :param code: 返回状态码 200成功 500失败
    :param message: 失败返回相应的失败信息 成功此字段为空
    :param data: 成功返回相应的数据 此字段是前后端数据交互的载体 失败此字段为空
    :return:
    """
    return jsonify({'status': code, 'message': message, 'data': data})
