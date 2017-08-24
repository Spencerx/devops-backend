#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson as simplejson

from app.models.workflows import Workflow
from flask import Blueprint, jsonify, request
from app.tools.redisUtils import create_redis_connection
from app.tools.jsonUtils import response_json
import datetime

workflow = Blueprint('workflow',__name__)

@workflow.route('/history')
def history():
    r = create_redis_connection()
    table_data = r.lrange('workflow_history_tabledata',0,-1)
    if table_data:
        print 'come from redis'
        json_table_data = []
        for table in table_data:
            json_table_data.append(eval(table))
        return jsonify(json_table_data)
    else:
        print 'come from mysql'
        all_workflow = Workflow.select()
        data = []
        for workflow in all_workflow:
            per_flow = {
                    'ID':workflow.w,
                    'create_time':workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                    'close_time':workflow.close_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.close_time else '',
                    'team_name':workflow.team_name,
                    'dev_user':workflow.dev_user,
                    'test_user':workflow.test_user,
                    'sql_info':workflow.sql_info,
                    'production_user':workflow.production_user,
                    'current_version':workflow.current_version,
                    'last_version':workflow.last_version,
                    'comment':workflow.comment,
                    'deploy_info':workflow.deploy_info,
                    'status':workflow.status,
                    'service':workflow.service,
                    'approved_user':workflow.approved_user,
                 }
            r.rpush('workflow_history_tabledata',per_flow)
            data.append(per_flow)
        r.expire('workflow_history_tabledata',60)
        return jsonify(data)

@workflow.route('/history/search',methods=['POST','OPTION'])
def workflow_history_search():
    if request.method == 'POST':
        form_data = request.get_json()
        id = form_data['id']
        team = form_data['team']
        create_date = form_data['create_time']
        is_deploy = form_data['is_deploy']
        print team,create_date
        if id:
            try:
                workflow = Workflow.select().where(Workflow.w==id).get()
            except Exception,e:
                return ''
            data = []
            per_flow = {
                'ID': workflow.w,
                'date': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'team_name': workflow.team_name,
                'dev_user': workflow.dev_user,
                'test_user': workflow.test_user,
                'sql_info': workflow.sql_info,
                'production_user': workflow.production_user,
                'jenkins_version': workflow.jenkins_version,
                'v_version': workflow.v_version,
                'last_jenkins_version': workflow.last_jenkins_version,
                'comment': workflow.comment,
                'status': workflow.comment
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
            return response_json(200,'create successful')
        except Exception,e:
            return response_json(500,'create failed')
    else:
        return ''
