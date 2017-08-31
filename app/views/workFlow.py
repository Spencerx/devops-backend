#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models.workflows import Workflow
from flask import Blueprint, jsonify, request
from app.tools.redisUtils import create_redis_connection
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user, user_to_id, service_to_id, status_to_id, team_to_id
from app.tools.ormUtils import id_to_service
from app.tools.ormUtils import id_to_team
from app.tools.ormUtils import id_to_status
from app.tools.commonUtils import async_send_email
from app.models.users import Users
import datetime

workflow = Blueprint('workflow',__name__)


@workflow.route('/history', methods=["GET", "POST"])
def history():
    if request.method == 'POST':
        form_data = request.get_json()
        per_size = form_data['size']
        page_count = form_data['page']
        if page_count == 0:
            ws = Workflow.select().limit(10)
        else:
            ws = Workflow.select().limit(int(per_size)).offset((int(page_count)-1)*int(per_size))
        data = []
        for workflow in ws:
            per_flow = {
                'ID': workflow.w,
                'create_time': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'close_time': workflow.close_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.close_time else '',
                'team_name': id_to_team(workflow.team_name),
                'dev_user': id_to_user(workflow.dev_user),
                'test_user': id_to_user(workflow.test_user),
                'sql_info': workflow.sql_info,
                'production_user': id_to_user(workflow.production_user),
                'current_version': workflow.current_version,
                'last_version': workflow.last_version,
                'comment': workflow.comment,
                'deploy_info': workflow.deploy_info,
                'status': workflow.status,
                'status_info': id_to_status(workflow.status),
                'service': id_to_service(workflow.service) if workflow.service else '',
                'approved_user': id_to_user(workflow.approved_user) if workflow.approved_user else '',
                'ops_user': id_to_user(workflow.ops_user) if workflow.ops_user else '',
            }
            data.append(per_flow)
        workflow_count = Workflow.select().count()
        return response_json(200, '', {"count": workflow_count, "data": data})


@workflow.route('/history/search',methods=['POST','OPTION'])
def workflow_history_search():
    if request.method == 'POST':
        form_data = request.get_json()
        id = form_data['id']
        team = form_data['team']
        create_time = form_data['create_time']
        is_deploy = form_data['is_deploy']
        if id:
            try:
                workflow = Workflow.select().where(Workflow.w==id).get()
            except Exception,e:
                return response_json(200,'','')
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
                'approved_user':workflow.approved_user
            }
            data.append(per_flow)
            if data:
                return jsonify(data)
            else:
                return jsonify('')
        else:
            pass
            # workflow = Workflow.select().where(Workflow.team_name).get()

    else:
        return ''


@workflow.route('/create', methods=['POST', 'OPTION'])
def create_workflow():
    if request.method == 'POST':
        form_data = request.get_json()
        service = form_data['service']
        team_name = form_data['team_name']
        dev_user = user_to_id(form_data['dev_user'])
        test_user = user_to_id(form_data['test_user'])
        production_user = user_to_id(form_data['production_user'])
        current_version = form_data['current_version']
        last_version = form_data['last_version']
        sql_info = form_data['sql_info']
        comment = form_data['comment']
        deploy_info = form_data['deploy_info']
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        w = Workflow(service=service, create_time=create_time,
                     dev_user=dev_user, test_user=test_user, production_user=production_user,
                     current_version=current_version, last_version=last_version, sql_info=sql_info,
                     team_name=team_name, comment=comment, deploy_info=deploy_info)

        try:
            w.save()
            w_id = w.w
            email_data = {
                "service": id_to_service(service),
                "team_name": id_to_team(service),
                "dev_user": dev_user,
                "test_user": test_user,
                "production_user": production_user,
                "current_version": current_version,
                "last_version": last_version,
                "sql_info": sql_info,
                "comment": comment,
                "create_time": create_time,
                "deploy_info": deploy_info,
                "id": w_id,
            }

            approved_users = Users.select().where(Users.can_approved == 1)
            to_list = [approved_user.email for approved_user in approved_users]
            async_send_email(to_list, u"上线审批", email_data, e_type="approve")
            return response_json(200, '', 'ceate successful')
        except Exception, e:
            print e
            return response_json(500, 'create failed', '')
    else:
        return ''


@workflow.route('/myflow', methods=['POST', 'OPTION'])
def my_flow():
    if request.method == "POST":
        req_data = request.get_json()
        uid = req_data['uid']
        u = Users.select().where(Users.id == uid).get()
        user_role = u.role
        can_approved = u.can_approved
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
            return response_json(200, "", [])
        else:
            flow_data = []
            for flow_id in workflow_list:
                flows = Workflow.select().where(Workflow.w == flow_id)
                for per_flow in flows:
                    per_flow_data = {
                        'ID': per_flow.w,
                        'create_time': per_flow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                        'team_name': per_flow.team_name,
                        'sql_info': per_flow.sql_info if per_flow.sql_info else '',
                        'test_user': id_to_user(per_flow.test_user) if per_flow.test_user else '',
                        'dev_user': id_to_user(per_flow.dev_user) if per_flow.dev_user else '',
                        'current_version': per_flow.current_version,
                        'comment': per_flow.comment if per_flow.comment else '',
                        'deploy_info': per_flow.deploy_info,
                        'service': per_flow.service,
                        'status_info': id_to_status(per_flow.status),
                        'status': per_flow.status,
                    }
                    flow_data.append(per_flow_data)
            flow_count = len(flow_data)
            return response_json(200, "", {'data': flow_data, 'count': flow_count})

    else:
        return ''
