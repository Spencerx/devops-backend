#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
from requests.exceptions import Timeout
from json import JSONEncoder
from urlparse import urljoin
from flask import Blueprint, request, current_app
from app.models.services import Services
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user, user_to_id
from app.tools.switchflowUtils import registed_service
from app.wrappers.permission import manager_required

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
                services = Services.select().order_by(Services.service_status.desc())
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
                    'is_switch_flow': True if int(s.is_switch_flow) == 1 else False
                }
                data.append(per_team)
            return response_json(200, "", data=data)
        except Exception, e:
            current_app.logger.error("get all service failed message:{0}".format(e))
            return response_json(500, e, "")
    else:
        return response_json(200, "", "")


@service.route('/create_service', methods=["POST"])
@manager_required
def create_service():
    if request.method == "POST":
        json_data = request.get_json()
        service_name = json_data['service_name']
        service_leader = user_to_id(json_data['service_leader'])
        desc = json_data['desc']
        language = json_data['language']
        s = Services(service_name=service_name, comment=desc, service_leader=service_leader,
                     create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     language=language, service_status='1')
        try:
            s.save()
            return response_json(200, '', '')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, '', '')


@service.route('/update_service', methods=['POST'])
@manager_required
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
        is_switch_flow = json_data['is_switch_flow']
        is_active = json_data['is_active']
        try:
            s = Services.select().where(Services.s == int(service_id)).get()
            s.service_name = service_name
            s.service_leader = service_leader
            s.comment = comment
            s.type = service_type
            s.language = language
            s.is_switch_flow = 1 if is_switch_flow else 2
            s.service_status = "1" if is_active else "0"
            s.save()
            return response_json(200, '', 'modify service success')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return response_json(200, '', '')


@service.route('/upstream/switch_flow_on', methods=['POST'])
@manager_required
def switch_flow_on():
    """
    放流 nginx upstream开启对应的backend的流量
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        try:
            service_name = json_data['service']
            ip = json_data['row']['ip']
            port = str(json_data['row']['port'])
            attribute = json_data['row']['attribute']
            attribute['down'] = 0
            attribute = JSONEncoder().encode(attribute)
            r = requests.put(urljoin(current_app.config['CONSUL_BASE_URL'], "upstreams/{0}/{1}".
                                     format(service_name, ip+":"+port)), data=str(attribute))
            if r.status_code == 200:
                return response_json(200, '', u'开启流量成功')
            else:
                return response_json(500, u'开启流量失败', '')
        except Timeout, e:
            current_app.logger.error(e)
            return response_json(500, u'consul api time out')

    else:
        pass


@service.route('/upstream/switch_flow_off', methods=['POST'])
@manager_required
def switch_flow_off():
    """
    关流 nginx upstream关闭对应的backend的流量
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        try:
            service_name = json_data['service']
            ip = json_data['row']['ip']
            port = str(json_data['row']['port'])
            attribute = json_data['row']['attribute']
            attribute['down'] = 1
            attribute = JSONEncoder().encode(attribute)
            r = requests.put(urljoin(current_app.config['CONSUL_BASE_URL'], "upstreams/{0}/{1}".
                                     format(service_name, ip+":"+port)), data=str(attribute))
            if r.status_code == 200:
                return response_json(200, '', u'关闭流量成功')
            else:
                return response_json(500, u'关闭流量失败', '')
        except Timeout, e:
            current_app.logger.error(e)
            return response_json(500, u'consul api time out')

    else:
        return response_json(200, '', '')


@service.route('/upstream/switch_flow_double_weight', methods=['POST'])
@manager_required
def switch_flow_double_weight():
    """
    upstream下的指定机器权重weight加倍 倍权
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        try:
            service_name = json_data['service']
            ip = json_data['row']['ip']
            port = str(json_data['row']['port'])
            attribute = json_data['row']['attribute']
            if int(attribute['weight']) == 1 or int(attribute['weight']) == 2:
                attribute['weight'] = int(attribute['weight'])*2
            else:
                return response_json(500, u'权重已经为最高', '')
            attribute = JSONEncoder().encode(attribute)
            r = requests.put(urljoin(current_app.config['CONSUL_BASE_URL'], "upstreams/{0}/{1}".
                                     format(service_name, ip + ":" + port)), data=str(attribute))
            if r.status_code == 200:
                return response_json(200, '', u'倍权成功')
            else:
                return response_json(500, u'倍权失败', '')
        except Timeout, e:
            current_app.logger.error(e)
            return response_json(500, u'consul api time out')
    else:
        return response_json(200, '', '')


@service.route('/upstream/switch_flow_half_weight', methods=['POST'])
@manager_required
def switch_flow_half_weight():
    """
    upstream下的指定机器权重weight减半 半权
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        try:
            service_name = json_data['service']
            ip = json_data['row']['ip']
            port = str(json_data['row']['port'])
            attribute = json_data['row']['attribute']
            if int(attribute['weight']) == 2 or int(attribute['weight']) == 4:
                attribute['weight'] = int(attribute['weight'])/2
            else:
                return response_json(500, u'权重已经为最低', '')
            attribute = JSONEncoder().encode(attribute)
            r = requests.put(urljoin(current_app.config['CONSUL_BASE_URL'], "upstreams/{0}/{1}".
                                     format(service_name, ip + ":" + port)), data=str(attribute))
            if r.status_code == 200:
                return response_json(200, '', u'半权成功')
            else:
                return response_json(500, u'半权失败', '')
        except Timeout, e:
            current_app.logger.error(e)
            return response_json(500, u'consul api time out')
    else:
        return response_json(200, '', '')


@service.route('/all_backend_info')
def all_registed_service_backend_info():
    """
    获取所有切流量服务的backend信息接口
    :return:
    """
    backends = registed_service(scope='all')
    return response_json(200, '', data=backends)


@service.route('/destined_backend_info', methods=["POST"])
def destined_registed_service_backend_info():
    """
    获取指定服务名的backend信息接口
    :return:
    """
    if request.method == "POST":
        service_name = request.get_json()['service']
        backends = registed_service(scope='per', service=service_name)
        return response_json(200, '', data=backends)
    else:
        response_json(200, '', '')


@service.route('update_backend_server')
def update_backend_server():
    """
    更新服务对应的后端机器列表
    :return:
    """
    if request.method == "POST":
        pass
    else:
        return response_json(200, '', '')

