#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from app.models.workflows import Workflow
from app.models.users import Users
from app.models.flow_type import FlowTyle
from app.models.services import Services
from flask import Blueprint, request
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user, id_to_service, id_to_team, id_to_status, id_to_flow_type, service_to_id, querylastversion_by_id
from app.tools.commonUtils import async_send_email


workflow = Blueprint('workflow', __name__)


@workflow.route('/history', methods=["GET", "POST"])
def history():
    """
    获取历史工作流接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        per_size = form_data['size']
        page_count = form_data['page']
        if page_count == 0:
            ws = Workflow.select().limit(10).order_by(Workflow.w.desc())
        else:
            ws = Workflow.select().limit(int(per_size)).offset((int(page_count)-1)*int(per_size)).\
                order_by(Workflow.w.desc())
        data = []
        for workflow in ws:
            per_flow = {
                'ID': workflow.w,
                'create_time': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'deploy_start_time': workflow.deploy_start_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.deploy_start_time else '',
                'deploy_end_time': workflow.deploy_end_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.deploy_end_time else '',
                'close_time': workflow.close_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.close_time else '',
                'team_name': id_to_team(workflow.team_name),
                'dev_user': id_to_user(workflow.dev_user),
                'test_user': id_to_user(workflow.test_user),
                'create_user': id_to_user(workflow.create_user),
                'sql_info': workflow.sql_info,
                'production_user': id_to_user(workflow.production_user),
                'flow_type': id_to_flow_type(workflow.type),
                'current_version': workflow.current_version,
                'last_version': querylastversion_by_id(workflow.service),
                'comment': workflow.comment,
                'deploy_info': workflow.deploy_info,
                'status': workflow.status,
                'status_info': id_to_status(workflow.status),
                'service': id_to_service(workflow.service) if workflow.service else '',
                'approved_user': id_to_user(workflow.approved_user) if workflow.approved_user else '',
                'ops_user': id_to_user(workflow.ops_user) if workflow.ops_user else '',
                'config': workflow.config if workflow.config else '',
                'deny_info': workflow.deny_info if workflow.deny_info else '',
                'access_info': workflow.access_info if workflow.access_info else '',
            }
            data.append(per_flow)
        workflow_count = Workflow.select().count()
        return response_json(200, '', {"count": workflow_count, "data": data})


@workflow.route('/history/search', methods=['POST', 'OPTION'])
def workflow_history_search():
    # todo
    """
    历史工作流按照条件搜索接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        id = form_data['id']
        team = form_data['team']
        create_time = form_data['create_time']
        is_deploy = form_data['is_deploy']
        if id:
            try:
                workflow = Workflow.select().where(Workflow.w == id).get()
            except Exception, e:
                print e
                return response_json(200, '', {'count': 0, 'data': []})
            data = []
            per_flow = {
                'ID': workflow.w,
                'create_time': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'team_name': workflow.team_name,
                'dev_user': workflow.dev_user,
                'test_user': workflow.test_user,
                'sql_info': workflow.sql_info,
                'production_user': workflow.production_user,
                'current_version': workflow.current_version,
                'last_version': workflow.last_version,
                'comment': workflow.comment,
                'deploy_info': workflow.deploy_info,
                'service': workflow.service,
                'status': workflow.status,
                'status_info': id_to_status(workflow.status),
                'approved_user': workflow.approved_user
            }
            data.append(per_flow)
            flow_count = len(data)
            return response_json(200, '', {'count': flow_count, 'data': data})
        else:
            pass
    else:
        return ''


@workflow.route('/create', methods=['POST', 'OPTION'])
def create_workflow():
    """
    新建工作流接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        flow_type = form_data['flow_type']
        utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        approved_users = Users.select().where(Users.can_approved == '1')
        to_list = [approved_user.email for approved_user in approved_users]
        # 判断工作流类型 来区分处理逻辑
        # 系统上线
        if flow_type == 1:
            services = form_data['service']
            mail_services = ''
            mail_ids = ''
            mail_versions = ''
            team_name = form_data['team_name']
            dev_user = int(form_data['dev_user'])
            test_user = int(form_data['test_user'])
            create_user = form_data['create_user']
            production_user = int(form_data['production_user'])
            sql_info = form_data['sql_info']
            deploy_start_time = datetime.datetime.strptime(form_data['deploy_time'][0], utc_format). \
                strftime('%Y-%m-%d %H:%M:%S')
            deploy_end_time = datetime.datetime.strptime(form_data['deploy_time'][1], utc_format). \
                strftime('%Y-%m-%d %H:%M:%S')
            comment = form_data['comment']
            deploy_info = form_data['deploy_info']
            config = form_data['config']
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for service in services:
                service_name = service['service']
                version = service['version']
                mail_services = mail_services + service_name + " "
                mail_versions = mail_versions + version + " "
                w = Workflow(service=service_to_id(service_name), create_time=create_time,
                             dev_user=dev_user, test_user=test_user, production_user=production_user,
                             current_version=version, type=flow_type, deploy_start_time=deploy_start_time,
                             sql_info=sql_info, team_name=team_name, comment=comment, deploy_end_time=deploy_end_time,
                             deploy_info=deploy_info, config=config, create_user=create_user)
                w.save()
                w_id = w.w
                mail_ids = mail_ids + str(w_id) + " "
            email_data = {
                "service": mail_services,
                "version": mail_versions,
                "team_name": id_to_team(team_name),
                "dev_user": id_to_user(dev_user),
                "test_user": id_to_user(test_user),
                "production_user": id_to_user(production_user),
                "sql_info": sql_info,
                "comment": comment,
                "create_time": create_time,
                "deploy_info": deploy_info,
                "config": config,
                "id": mail_ids,
            }
            async_send_email(to_list, u"上线审批", email_data, e_type=flow_type)
            return response_json(200, '', 'ceate successful')

        # 数据库变更
        elif flow_type == 2:
            team_name = form_data['team_name']
            test_user = int(form_data['test_user'])
            create_user = form_data['create_user']
            sql_info = form_data['sql_info']
            comment = form_data['comment']
            deploy_start_time = datetime.datetime.strptime(form_data['deploy_time'][0], utc_format).\
                strftime('%Y-%m-%d %H:%M:%S')
            deploy_end_time = datetime.datetime.strptime(form_data['deploy_time'][1], utc_format).\
                strftime('%Y-%m-%d %H:%M:%S')
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w = Workflow(create_time=create_time, test_user=test_user, type=flow_type,
                         sql_info=sql_info, team_name=team_name, comment=comment, create_user=create_user,
                         deploy_start_time=deploy_start_time, deploy_end_time=deploy_end_time)
            w.save()
            w_id = w.w
            email_data = {
                "team_name": id_to_team(team_name),
                "test_user": id_to_user(test_user),
                "sql_info": sql_info,
                "comment": comment,
                "create_time": create_time,
                "deploy_start_time": deploy_start_time,
                "deploy_end_time": deploy_end_time,
                "id": w_id,
            }
            async_send_email(to_list, u"数据库变更审批", email_data, e_type=flow_type)
            return response_json(200, '', 'ceate successful')

        # 配置变更
        elif flow_type == 3:
            service = form_data['service']
            team_name = form_data['team_name']
            test_user = int(form_data['test_user'])
            create_user = form_data['create_user']
            sql_info = form_data['sql_info']
            config = form_data['config']
            comment = form_data['comment']
            deploy_start_time = form_data['deploy_time'][0]
            deploy_end_time = form_data['deploy_time'][1]
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w = Workflow(service=service, create_time=create_time, test_user=test_user, type=flow_type,
                         sql_info=sql_info, team_name=team_name, comment=comment, create_user=create_user,
                         deploy_start_time=deploy_start_time, deploy_end_time=deploy_end_time)
            w.save()
            w_id = w.w
            email_data = {
                "service": id_to_service(service),
                "team_name": id_to_team(team_name),
                "test_user": id_to_user(test_user),
                "sql_info": sql_info,
                "comment": comment,
                "create_time": create_time,
                "config": config,
                "id": w_id,
            }
            async_send_email(to_list, u"配置变更审批", email_data, e_type="approve")
            return response_json(200, '', 'ceate successful')

        # 权限申请
        elif flow_type == 4:
            pass

        # 不明确的工作流类型
        else:
            return response_json(500, u'工作流类型不明确', '')
    else:
        return ''


@workflow.route('/myflow', methods=['POST', 'OPTION'])
def my_flow():
    """
    获取需要当前用户处理的工作流
    :return:
    """
    if request.method == "POST":
        req_data = request.get_json()
        uid = req_data['uid']
        u = Users.select().where(Users.id == uid).get()
        user_role = u.role
        can_approved = int(u.can_approved)
        workflow_list = []
        if int(user_role) == 2:
            flows = Workflow.select().where(Workflow.status == 2)
            for flow in flows:
                workflow_list.append(flow.w)

        if int(user_role) == 4:
            flows = Workflow.select().where((Workflow.status == 3) & (Workflow.test_user == uid))
            for flow in flows:
                workflow_list.append(flow.w)

        if can_approved:
            flows = Workflow.select().where(Workflow.status == 1)
            for flow in flows:
                workflow_list.append(flow.w)

        if not workflow_list:
            return response_json(200, "", {'data': [], 'count': 0})
        else:
            flow_data = []
            for flow_id in workflow_list:
                flows = Workflow.select().where(Workflow.w == flow_id)
                for per_flow in flows:
                    per_flow_data = {
                        'ID': per_flow.w,
                        'create_time': per_flow.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'team_name': per_flow.team_name,
                        'sql_info': per_flow.sql_info if per_flow.sql_info else '',
                        'test_user': id_to_user(per_flow.test_user) if per_flow.test_user else '',
                        'create_user': id_to_user(per_flow.create_user) if per_flow.create_user else '',
                        'dev_user': id_to_user(per_flow.dev_user) if per_flow.dev_user else '',
                        'current_version': per_flow.current_version,
                        'comment': per_flow.comment if per_flow.comment else '',
                        'deploy_info': per_flow.deploy_info,
                        'service': id_to_service(per_flow.service),
                        'status_info': id_to_status(per_flow.status),
                        'status': per_flow.status,
                        'config': per_flow.config if per_flow.config else '',
                        'flow_type': id_to_flow_type(per_flow.type),
                    }
                    flow_data.append(per_flow_data)
            flow_count = len(flow_data)
            return response_json(200, "", {'data': flow_data, 'count': flow_count})

    else:
        return ''


@workflow.route('/approved', methods=['POST', 'OPTION'])
def approved():
    """
    工作流审批接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        approved = json_data['approved']
        suggestion = json_data['suggestion']
        uid = json_data['uid']
        w_id = json_data['w_id']
        w = Workflow.select().where(Workflow.w == w_id).get()
        if approved == "access":
            if int(w.status) != 1:
                return response_json(301, '', u'工作流状态检测到已经被改变')
            w.status = int(w.status) + 1
            w.access_info = suggestion
            w.approved_user = uid
            w.save()
            return response_json(200, "", "")
        elif approved == "deny":
            if int(w.status) != 1:
                return response_json(301, '', u'工作流状态检测到已经被改变')
            w.status = 5
            w.approved_user = uid
            w.deny_info = suggestion
            w.close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w.save()
            return response_json(200, "", "")
        else:
            return response_json(500, u"审批参数无效", "")
    else:
        return response_json(200, '', '')


@workflow.route('/sure_deploy', methods=['POST', 'OPTION'])
def sure_deploy():
    """
    确认工作流中服务上线接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        uid = json_data['uid']
        w_id = json_data['w_id']
        w = Workflow.select().where(Workflow.w == w_id).get()
        s = Services.select().where(Services.s == int(w.service)).get()
        if int(w.status) != 2:
            return response_json(301, '', u'工作流状态检测到已经被改变')
        s.current_version = w.current_version  # 修改该服务的最新版本为当前上线版本
        w.status = int(w.status) + 1
        w.ops_user = uid
        try:
            w.save()
            s.save()
            return response_json(200, '', '')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return ""


@workflow.route('/sure_test', methods=['POST', 'OPTION'])
def sure_test():
    """
    测试确认上线服务正常接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        w_id = json_data['w_id']
        w = Workflow.select().where(Workflow.w == w_id).get()
        if int(w.status) != 3:
            return response_json(301, '', u'工作流状态检测到已经被改变')
        w.status = int(w.status) + 1
        w.close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            w.save()
            return response_json(200, '', '')
        except Exception, e:
            return response_json(500, e, '')
    else:
        return ""


@workflow.route('/type')
def flow_type_list():
    """
    获取工作流所有类型接口
    :return:
    """
    ts = FlowTyle.select()
    data = []
    for t in ts:
        per_type = {
            'id': t.id,
            'type': t.type
        }
        data.append(per_type)
    return response_json(200, '', data=data)



