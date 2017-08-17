#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson as simplejson

from app.models.workflows import Workflow
from flask import Blueprint, jsonify, request
from app.tools.redisUtils import create_redis_connection


workflow = Blueprint('workflow',__name__)

@workflow.route('/history')
def history():
    print request.method
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

