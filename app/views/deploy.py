#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from json import JSONEncoder
from urlparse import urljoin
from requests.exceptions import Timeout
from flask import Blueprint, request, current_app
from app.tools.jsonUtils import response_json
from app.tools.saltUtils import generate_salt_token
from app.tools.connectpoolUtils import create_redis_connection
from app.tools.switchflowUtils import registed_service
from app.models.workflows import Workflow
from app.models.services import Services
from app.models.server import Servers
from app.models.service_server import ServiceBackend
from app.models import workflows
from app.models import services
import grpc
from app.protobufs.airflow_pb2 import ReqPingData, ReqCheckSvcData
from app.protobufs.airflow_pb2_grpc import PingStub, ServiceCheckStub

deploy = Blueprint("deploy", __name__)


@deploy.route("/deploy_info", methods=["POST"])
def deploy_info():
    if request.method == "POST":
        json_data = request.get_json()
        flow_id = json_data['wid']
        try:
            w = Workflow.select().where(Workflow.w == int(flow_id)).get()
        except workflows.DoesNotExist, _:
            return response_json(404, u'工作流不存在', '')

        # 判断该服务是否是系统上线
        if int(w.type) != 1:
            return response_json(500, u'检测工作流类型不为系统上线', '')

        # 判断该服务的状态是否为待部署
        if int(w.status) != 2:
            return response_json(500, u'检测工作流状态异常', '')
        else:
            try:
                service = Services.select().where((Services.s == w.service) & (Services.service_status == 1)).get()
            except services.DoesNotExist, _:
                return response_json(404, u'服务不存在或未激活', '')
            if service.is_switch_flow == 1:
                """切流量服务 在consul中查询backend"""
                backends = registed_service(scope='per', service=service.service_name.strip())
                if backends:
                    resp_data = {
                        "wid": w.w,
                        "service": service.service_name,
                        "is_switch_flow": u'是' if int(service.is_switch_flow) == 1 else u'否',
                        "version": w.current_version,
                        "last_version": w.last_version
                    }
                    backend_info = []
                    for server in backends[service.service_name.strip()]:
                        backend_info.append({"ip": server['ip'], "port": server['port'], "attr": resp_data})
                    return response_json(200, '', backend_info)
                else:
                    return response_json(500, u'该服务没有配置对应的upstream', '')
            else:
                """普通服务不切流量在数据库中查询backend"""
                backend_info = []
                servers = ServiceBackend.select().where(ServiceBackend.service == service.s)
                for server in servers:
                    backend_info.append({
                        'ip': Servers.select().where(Servers.id == server.server).get().internal_ip,
                        'port': server.port,
                        'attr': {
                            'is_switch_flow': u'是' if int(service.is_switch_flow) == 1 else u'否',
                            'version': service.current_version,
                            'service': service.service_name,
                            'last_version': service.current_version,
                            }
                    })
                return response_json(200, '', backend_info)
    else:
        return response_json(200, '', '')


@deploy.route("/check_env", methods=["POST"])
def check_env():
    """
    发布第一步:检测环境 确认目标机器上面部署了airflow的agent ping => pong
    :return:
    """
    if request.method == "POST":
        form_data = request.form.to_dict()  # Ajax json request
        _HOST = form_data['host']
        _PORT = '9999'
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        client = PingStub(channel=conn)
        try:
            response = client.Ping(ReqPingData(health_url=''))
        except Exception, _:
            return response_json(500, 'agent at {0} status is down'.format(_HOST), '')
        if response.status == "Pong":
            return response_json(200, '', 'Pong')
    else:
        return response_json(200, '', '')


@deploy.route("/deploy_switch_flow_off", methods=["POSt"])
def auto_switch_flow_off():
    """
    正式部署前 自动关闭流量
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        host = json_data["host"]
        port = json_data["port"]
        service = json_data["service"]
        backends = registed_service(scope='per', service=service)
        for backend in backends[service]:
            if backend['ip'] == host.strip() and backend['port'] == host.strip():
                attr = eval(backend['attribute'])
                attr['down'] = 1
                attribute = JSONEncoder().encode(attr)
                try:
                    r = requests.put(urljoin(current_app.config['CONSUL_BASE_URL'], "upstreams/{0}/{1}".
                                             format(service, host + ":" + port)), data=str(attribute))
                    if r.status_code == 200:
                        return response_json(200, '', u'关闭流量成功')
                    else:
                        return response_json(500, u'关闭流量失败', '')
                except Timeout, e:
                    current_app.logger.error(e)
                    return response_json(500, u'consul api time out')
        return response_json(500, 'host not find in consul', '')
    else:
        return response_json(200, '', '')


@deploy.route("/deploy_product", methods=["POST"])
def deploy_product():
    """
    正式部署 执行脚本
    :return:
    """
    if request.method == "POST":
        salt_token = generate_salt_token()
        json_data = request.get_json()
        script_target_path = current_app.config["DEPLOY_SCRIPTS_SAVE_PATH"]
        host = json_data['host']
        flow_id = json_data['flow_id']
    else:
        return response_json(200, '', '')


@deploy.route("/deploy_switch_flow_on")
def auto_switch_flow_on():
    """
    部署完成 自动开启流量
    :return:
    """
    pass


@deploy.route("/check_deploy", methods=["POST"])
def check_deploy():
    if request.method == "POST":
        json_data = request.get_json()
        _HOST = json_data['host']
        _HOST = '127.0.0.1'
        _PORT = '9999'
        conn = grpc.insecure_channel(_HOST + ':' + _PORT)
        check_url = 'http://baidu.com'
        cli_check = ServiceCheckStub(channel=conn)
        for count in range(3):
            try:
                res_check = cli_check.ServiceCheck(ReqCheckSvcData(health_url=check_url))
            except Exception, _:
                return response_json(500, 'check url has exception', '')
            else:
                if res_check.status == '200':
                    return response_json(200, 'service is healthy', '')
            import time
            time.sleep(3)
        return response_json(500, 'check service url timeout, service maybe is starting just now', '')
    else:
        return response_json(200, '', '')


@deploy.route("/show_deploy_log", methods=["POST"])
def show_deploy_log():
    """
    正式部署 日志实时查看
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        flow_id = json_data['flow_id']
        host = json_data['host']
        try:
            r = create_redis_connection()
            redis_resp = eval(r.hget(flow_id, host))
            resp = ""
            if redis_resp:
                for step in redis_resp:
                    step_key = step.keys()[0]
                    step_value = step[step_key]
                    resp = resp + "[" + step_key + "]" + "\n"+"\n"+step_value + "\n" + "\n" +"\n" +"\n" +"\n"
            return response_json(200, '', resp)
        except Exception, _:
            return response_json(500, 'connect redis exception', '')
    else:
        return response_json(200, '', '')


