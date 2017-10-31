#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import datetime
import requests
from json import JSONEncoder
from urlparse import urljoin
from requests.exceptions import Timeout
from flask import Blueprint, request, current_app
from app.tools.jsonUtils import response_json
from app.tools.saltUtils import generate_salt_token, exec_commands, ping_check, trans_file
from app.tools.redisUtils import create_redis_connection
from app.tools.switchflowUtils import registed_service
from app.models.workflows import Workflow
from app.models.services import Services
from app.models.scripts import Scripts
from app.models import workflows
from app.models import services
from simplejson.scanner import JSONDecodeError
from requests.exceptions import ReadTimeout

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
                    backend_info.append({"ip": server['ip'], "port": server['port'], "attr":resp_data})
                return response_json(200, '', backend_info)
            else:
                return response_json(500, u'该服务没有配置对应的upstream', '')
    else:
        return response_json(200, '', '')


@deploy.route("/check_env", methods=["POST"])
def check_env():
    """
    发布第一步:检测环境 确认目标机器在salt minion中 且test.ping 为True状态
    :return:
    """
    if request.method == "POST":
        salt_token = generate_salt_token()
        json_data = request.get_json()
        host = json_data['host']
        flow_id = json_data['flow_id']
        r = create_redis_connection()
        if salt_token:
            try:
                try:
                    res = ping_check(host=host, token=salt_token)
                except ReadTimeout, _:
                    r.hmset(flow_id, {host: {"step1": "salt api time out"}})
                    return response_json(500, u'salt api timeout,please check {0} salt status'.format(host), '')
                ret = res['return'][0][host]['ret']
                if ret:
                    if r.hget(flow_id, host):
                        r.hdel(flow_id, host)
                    r.hmset(flow_id, {host: [{"step1 {0}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
                                              'salt env check success'}]})
                    return response_json(200, '', ret)
                else:
                    return response_json(500, ret, '')
            except KeyError, _:
                r.hmset(flow_id, {"host": host, "step1": u'请确认主机 {0} 是否在salt列表中'.format(host)})
                return response_json(500, u'请确认主机 {0} 是否在salt列表中'.format(host), '')
            except JSONDecodeError, _:
                """salt-api被重启token会被重制, 程序读取存在redis中失效的token"""
                r.delete('salt_token')
                r.hmset(flow_id, {"host": host, "step1": "salt api may has restart,please try again"})
                return response_json(500, "salt api may has restart,please try again", '')
        else:
            r.hmset(flow_id, {"host": host, "step1": 'salt api has error'})
            current_app.logger.error("salt api has error")
            return response_json(500, "salt api has error", "")
    else:
        return response_json(200, '', '')


@deploy.route("/script_push_master", methods=["POST"])
def script_upload():
    """
    部署脚本推送salt master
    :return:
    """
    if request.method == "POST":
        r = create_redis_connection()
        json_data = request.get_json()
        host = json_data['host']
        flow_id = json_data['flow_id']
        script_target_path = current_app.config["DEPLOY_SCRIPTS_SAVE_PATH"]
        trans = paramiko.Transport(current_app.config['SALT_SSH_HOST'],
                                   current_app.config['SALT_SSH_PORT'])
        trans.connect(username=current_app.config['SALT_SSH_USER'],
                      password=current_app.config['SALT_SSH_PASSWD'])

        sftp = paramiko.SFTPClient.from_transport(trans)
        ssh = paramiko.SSHClient()
        ssh._transport = trans

        # 先检测master上面存放脚本的路径是否存在
        stdin, stdout, stderr = ssh.exec_command('ls {0}'.format(script_target_path))
        err = stderr.readlines()
        if len(err) != 0:
            ssh.exec_command('mkdir -p {0}'.format(script_target_path))
        try:
            script_name = str(flow_id) + "-" + \
                          datetime.datetime.now().strftime('%Y-%m-%d-%H:%M') + ".sh"
            deploy_script = r.hget(flow_id, "deploy_script_name")
            if deploy_script:
                pass
            else:
                w = Workflow.select().where(Workflow.w == int(flow_id)).get()
                print flow_id
                print flow_id
                print flow_id
                service_id = w.service
                s = Services.select().where(Services.s == int(service_id)).get()
                script_id = s.deploy_script
                sc = Scripts.select().where(Scripts.id == int(script_id)).get()
                script_content = sc.script_content
                with file(script_name, 'w') as f:
                    f.write(script_content)
                sftp.put(script_name, script_target_path + script_name)
                r.hset(flow_id, "deploy_script_path", script_name)
            ssh.exec_command('chmod +x {0}'.format(script_target_path)+script_name)
        except OSError, _:
            return response_json(500, u'脚本不存在', '')
        except IOError, _:
            # 预防上面mkdir命令执行
            return response_json(500, u'salt master 目标路径不存在', '')
        except Exception, e:
            print e.message
            pass
            return response_json(500, e, '')
        finally:
            trans.close()
            sftp.close()
        proccess_info = eval(r.hget(flow_id, host))
        proccess_info.append({"step2 {0}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
                              'push script to salt master success'})
        r.hmset(flow_id, {host: proccess_info})
        return response_json(200, '', 'push to master success')
    else:
        return response_json(200, '', '')


@deploy.route("/script_push_nodes", methods=["POST"])
def script_push_nodes():
    if request.method == "POST":
        salt_token = generate_salt_token()
        json_data = request.get_json()
        host = json_data['host']
        flow_id = json_data['flow_id']
        if salt_token:
            try:
                r = create_redis_connection()
                file_name = r.hget(flow_id, "deploy_script_path")
                res = trans_file(host=host, token=salt_token, file_name=file_name)
                ret = res['return'][0][host]['ret']
                retcode = res['return'][0][host]['retcode']
                # varify ret code
                if retcode == 0:
                    proccess_info = eval(r.hget(flow_id, host))
                    proccess_info.append({"step3 {0}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
                                          ret})
                    r.hmset(flow_id, {host: proccess_info})
                    return response_json(200, '', ret)
                else:
                    return response_json(500, ret, '')
            except JSONDecodeError, _:
                r = create_redis_connection()
                r.delete('salt_token')
                return response_json(500, "salt api may has restart,please try again", '')
        else:
            current_app.logger.error("salt api has error")
            return response_json(500, "salt api has error", "")

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
        if salt_token:
            try:
                r = create_redis_connection()
                script_name = r.hget(flow_id, "deploy_script_path")
                res = exec_commands(host=host, token=salt_token, cmd="chmod +x /opt/{0} && /opt/{1}".
                                    format(script_name, script_name))

                ret = res['return'][0][host]['ret']
                retcode = res['return'][0][host]['retcode']
                # varify ret code
                if retcode == 0:
                    proccess_info = eval(r.hget(flow_id, host))
                    proccess_info.append({"step4 {0}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
                                          ret})
                    r.hmset(flow_id, {host: proccess_info})
                    return response_json(200, '', ret)
                else:
                    return response_json(500, ret, '')
            except JSONDecodeError, _:
                r = create_redis_connection()
                r.delete('salt_token')
                return response_json(500, "salt api may has restart,please try again", '')
        else:
            current_app.logger.error("salt api has error")
            return response_json(500, "salt api has error", "")

    else:
        return response_json(200, '', '')


@deploy.route("/deploy_switch_flow_on")
def auto_switch_flow_on():
    """
    部署完成 自动开启流量
    :return:
    """
    pass


@deploy.route("/script_wrapper", methods=["POST"])
def script_wrapper():
    """
    部署完成 自动开启流量
    :return:
    """
    if request.method == "POST":
        a = request.get_json()
        code = a['code']
        with file("code.sh",'a+') as f:
            script = code.split("\n")
            ret = ""
            for i in script:
                if "$project" in i:
                    i = i.replace("$project", "haixue_test")
                    ret = ret + i+"\n"
                    continue
                if "$version" in i:
                    i = i.replace("$version", "1.0.1")
                    ret = ret + i + "\n"
                    continue
                ret = ret + i + "\n"
        return response_json(200, '', ret)
    else:
        return response_json(200, '', '')


@deploy.route("/check_deploy", methods=["POST"])
def check_deploy():
    if request.method == "POST":
        json_data = request.get_json()
        ip = json_data['host']
        flow_id = json_data['flow_id']
        port = json_data['port']
        redis = create_redis_connection()
        for i in range(3):
            import time
            time.sleep(2)
            print i+1
            try:
                r = requests.get("http://"+ip+":"+port+"/", headers={'host': 'www.a.com'})
                if r.status_code == 200:
                    proccess_info = eval(redis.hget(flow_id, ip))
                    proccess_info.append({"step5 {0}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
                                          "host {0} check status ok, status code is {1}".format(ip, r.status_code)})

                    redis.hmset(flow_id, {ip: proccess_info})
                    return response_json(200, '', r.status_code)
                else:
                    return response_json(500, r.status_code, '')
            except Exception, e:
                print e

                continue
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


