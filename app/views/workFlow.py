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
                    'date':workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                    'team_name':workflow.team_name,
                    'dev_name':workflow.dev_user,
                    'test_name':workflow.test_user,
                    'sql_info':workflow.sql_info,
                    'product_name':workflow.production_user,
                    'jenkins_version':workflow.jenkins_version,
                    'v_version':workflow.v_version,
                    'last_jenkins_version':workflow.last_jenkins_version,
                    'comment':workflow.comment,
                    'status':workflow.comment
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
        create_date = form_data['create_date']
        is_deploy = form_data['is_deploy']
        print team,create_date
        if id:
            try:
                workflow = Workflow.select().where(Workflow.w==id).get()
            except Exception,e:
                return ''
            print workflow
            data = []
            per_flow = {
                'ID': workflow.w,
                'date': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'team_name': workflow.team_name,
                'dev_name': workflow.dev_user,
                'test_name': workflow.test_user,
                'sql_info': workflow.sql_info,
                'product_name': workflow.production_user,
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
        form_data = request.form
        print form_data['service']
        print form_data
        #sql_state = form_data['sql_state']
        service = form_data['service']
        team = form_data['team']
        dev = form_data['dev']
        test = form_data['test']
        product = form_data['product']
        version = form_data['version']
        last_version = form_data['last_version']
        sql_desc = form_data['sql_desc']
        desc = form_data['desc']

        w = Workflow(service=service,comment=desc,create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     deploy_info=desc,dev_user=dev,test_user=test,production_user=product,jenkins_version=version,
                     last_jenkins_version=last_version,sql_info=sql_desc,team_name=team)

        w.save()
        return '200'
