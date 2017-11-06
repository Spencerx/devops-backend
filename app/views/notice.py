#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 平台首页的通知信息 redis作为存储介质 """
import uuid
import datetime
from flask import Blueprint, current_app, request
from app.tools.connectpoolUtils import create_redis_connection
from app.tools.jsonUtils import response_json

notice = Blueprint('notice', __name__)


@notice.route('/notice')
def notice_list():
    """
    从redis读取平台首页通知接口
    :return:
    """
    if request.method == "GET":
        try:
            r = create_redis_connection()
            data = []
            notices = r.hgetall('devops:index:notice')
            for n_id, value in notices.items():
                per_data = eval(value)
                per_data['id'] = n_id
                data.append(per_data)
            return response_json(200, '', data)
        except Exception, e:
            current_app.logger.error("load all index notice in redis has error message:{0}".format(e.message))
            return response_json(500, e.message, '')
    else:
        return response_json(200, '', '')


@notice.route('/create_notice', methods=['POST'])
def create_notice():
    """
    新增平台首页通知接口
    :return:
    """
    if request.method == "POST":
        try:
            content = request.get_json()['content']
            notice_id = uuid.uuid1()
            r = create_redis_connection()
            r.hset('devops:index:notice', notice_id, {'data': content, 'create_time':
                                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

            return response_json(200, '', '')
        except Exception, e:
            current_app.logger.error("create new notice in redis has error message:{0}".format(e.message))
            return response_json(500, e.message, '')
    else:
        return response_json(200, '', '')


@notice.route('/update_notice', methods=['POST'])
def update_notice():
    """
    修改平台首页通知接口
    :return:
    """
    if request.method == "POST":
        try:
            content = request.get_json()['new_content']
            notice_id = request.get_json()['n_id']
            r = create_redis_connection()
            res = r.hget('devops:index:notice', notice_id)
            if res:
                res = eval(res)
                data = {'create_time': res['create_time'], 'data': content}
                r.hset('devops:index:notice', notice_id, data)
                return response_json(200, '', '')
            else:
                return response_json(500, u'公告不存在', '')
        except Exception, e:
            current_app.logger.error("update notice in redis has error message:{0}".format(e))
            return response_json(500, e.message, '')
    else:
        return response_json(200, '', '')


@notice.route('/delete_notice', methods=['POST'])
def delete_notice():
    """
    删除平台首页通知
    :return:
    """
    if request.method == "POST":
        try:
            notice_id = request.get_json()['n_id']
            r = create_redis_connection()
            r.hdel('devops:index:notice', notice_id)
            return response_json(200, '', '')
        except Exception, e:
            current_app.logger.error("delete notice in redis has error message:{0}".format(e))
            return response_json(500, e.message, '')
    else:
        return response_json(200, '', '')

