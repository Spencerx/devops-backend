#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from app.models.scripts import Scripts
from app.models import scripts
from app.tools.jsonUtils import response_json
script = Blueprint('script', __name__)


@script.route('/scripts')
def script_list():
    """
    获取所有脚本接口
    :return:
    """
    scripts = Scripts.select()
    resp = []
    for s in scripts:
        per_res = {
            'id': s.id,
            'script_name': s.script_name,
            'script_content': s.script_content,
            'comment': s.comment,
            'type': s.type
        }
        resp.append(per_res)
    return response_json(200, '', resp)


@script.route('/create_script', methods=["POST"])
def create_script():
    """
    新建脚本接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        code = json_data['code']
        comment = json_data['comment']
        language = json_data['language']
        script_name = json_data['script_name']
        try:
            count = Scripts.select().where(Scripts.script_name == script_name).count()
            if count < 1:
                s = Scripts(script_name=script_name, type=language, comment=comment, script_content=code)
                s.save()
                return response_json(200, '', u'创建成功')
            else:
                return response_json(500, u'脚本名 {0} 已存在'.format(script_name), '')
        except scripts.DoesNotExist, _:
            return response_json(500, 'id {0} of script not found'.format('s'), '')
    else:
        return response_json(200, '', '')


@script.route('/update_script', methods=["POST"])
def update_script():
    """
    修改脚本接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        s_id = json_data['id']
        code = json_data['code']
        comment = json_data['comment']
        language = json_data['type']
        script_name = json_data['script_name']
        try:
            script = Scripts.select().where(Scripts.id == int(s_id)).get()
            script.script_content = code
            script.script_name = script_name
            script.type = language
            script.comment = comment
            script.save()
        except scripts.DoesNotExist, _:
            return response_json(500, 'id {0} of script not found'.format(s_id), '')
        return response_json(200, '', u'修改成功')
    else:
        return response_json(200, '', '')
