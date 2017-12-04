#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from app.tools.jsonUtils import response_json
from app.tools.dateUtils import last_week_date
from app.models.workflows import Workflow
import datetime
report = Blueprint("report", __name__)


@report.route('/overview')
def overview():
    """
    获取上周上线次数 天数为纬度
    :return: like: [10,34,56,23,10]
    """
    last_deploy_flow_count = []
    last_week_date_res = last_week_date()
    for index, value in enumerate(last_week_date_res):
        if index != len(last_week_date_res)-1:
            start_date = datetime.datetime.strptime(value, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(last_week_date_res[index+1], "%Y-%m-%d")
            w_count = Workflow.select().where((Workflow.create_time.between(start_date, end_date)) &
                                              (Workflow.type == 1)).count()
            last_deploy_flow_count.append(w_count)
    return response_json(200, '', last_deploy_flow_count)


@report.route('/overview/table')
def overview_table():
    """
    获取上周上线详情 天数为纬度
    :return:
    """
    last_deploy_flow = []
    last_week_date_res = last_week_date()
    for index, value in enumerate(last_week_date_res):
        if index != len(last_week_date_res)-1:
            start_date = datetime.datetime.strptime(value, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(last_week_date_res[index+1], "%Y-%m-%d")
            total_count = Workflow.select().where((Workflow.create_time.between(start_date, end_date)) &
                                                  (Workflow.type == 1)).count()
            # open flow
            open_count = Workflow.select().where((Workflow.create_time.between(start_date, end_date)) &
                                                 (Workflow.type == 1) & (Workflow.status == 3)).count()

            # success flow
            success_count = Workflow.select().where((Workflow.create_time.between(start_date, end_date)) &
                                                    (Workflow.type == 1) & (Workflow.status == 4)).count()
            # abort flow
            abort_count = Workflow.select().where((Workflow.create_time.between(start_date, end_date)) &
                                                  (Workflow.type == 1) & (Workflow.status == 5)).count()

            # except flow
            except_count = Workflow.select().where((Workflow.create_time.between(start_date, end_date)) &
                                                   (Workflow.type == 1) & (Workflow.status == 6)).count()
            last_deploy_flow.append({'date': value,
                                     'total': total_count,
                                     'success': success_count,
                                     'abort': abort_count,
                                     'except': except_count,
                                     'open': open_count})
    return response_json(200, '', last_deploy_flow)
