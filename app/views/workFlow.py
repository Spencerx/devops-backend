#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models.workflows import Workflow
from flask import Blueprint, jsonify, request
from app.tools.redisUtils import create_redis_connection
from app.tools.jsonUtils import response_json
from app.tools.ormUtils import id_to_user
from app.tools.ormUtils import id_to_service
from app.tools.ormUtils import id_to_team
from app.tools.ormUtils import id_to_status
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
                'service': id_to_service(workflow.service),
                'approved_user': id_to_user(workflow.approved_user),
                'ops_user': id_to_user(workflow.ops_user),
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
                'date': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
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
                'approved_user':workflow.approved_user
            }
            data.append(per_flow)
            if data:
                return jsonify(data)
            else:
                return jsonify('')
        else:
            return ''
    else:
        return ''

@workflow.route('/create',methods=['POST','OPTION'])
def create_workflow():
    if request.method == 'POST':
        form_data = request.get_json()
        service = form_data['service']
        team_name = form_data['team_name']
        dev_user = form_data['dev_user']
        test_user = form_data['test_user']
        production_user = form_data['production_user']
        current_version = form_data['current_version']
        last_version = form_data['last_version']
        sql_info = form_data['sql_info']
        comment = form_data['comment']
        deploy_info = form_data['deploy_info']

        w = Workflow(service=service,create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     dev_user=dev_user,test_user=test_user,production_user=production_user,current_version=current_version,last_version=last_version,
                     sql_info=sql_info,team_name=team_name,comment=comment,deploy_info=deploy_info)

        try:
            w.save()
            return response_json(200,'','ceate successful')
        except Exception,e:
            return response_json(500,'create failed','')
    else:
        return ''
