#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, current_app
from app.models.services import Services
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user

service = Blueprint('service', __name__)


@service.route('/service')
def service_list():
    """
        查询团队 is_filter_disactived来判断是否返回未激活的服务
        :return:
        """
    if request.method == "GET":
        try:
            if request.args.get("is_filter_disactived", None):
                services = Services.select().where(Services.service_status == 1)
            else:
                services = Services.select()
            data = []
            for s in services:
                per_team = {
                    'id': s.s,
                    'service_name': s.service_name,
                    'type': s.type,
                    'comment': s.comment if s.comment else '',
                    'create_time': s.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                    'service_leader': id_to_user(s.service_leader),
                    "language": s.language,
                    'service_status': u'激活' if int(s.service_status) == 1 else u"未激活",
                }
                data.append(per_team)
            return response_json(200, "", data=data)
        except Exception, e:
            current_app.logger.error("get all service failed message:{0}".format(e))
            return response_json(500, e, "")
    else:
        return response_json(200, "", "")


@service.route('/update_service', methods=['POST'])
def update_service():
    """
    修改服务配置接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        service_id = json_data['s_id']
        service_name = json_data['service_name']
        service_leader = json_data['service_leader']
        service_type = json_data['type']
        comment = json_data['comment']
        language = json_data['language']
        try:
            s = Services.select().where(Services.s == int(service_id)).get()
            s.service_name = service_name
            s.service_leader = service_leader
            s.comment = comment
            s.type = service_type
            s.language = language
            s.save()
            return response_json(200, '', 'modify service success')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, '', '')


@service.route('/active_delete_service', methods=['POST'])
def active_delete_servie():
    """
    禁用或者激活服务配置接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        service_id = json_data['s_id']
        try:
            s = Services.select().where(Services.s == int(service_id)).get()
            current_status = s.service_status
            if int(current_status) == 1:
                s.service_status = '0'
            else:
                s.service_status = '1'
            s.save()
            return response_json(200, '', 'modify service success')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, '', '')
