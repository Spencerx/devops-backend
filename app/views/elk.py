#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from app.tools.elasticsearchUtils import init_es_connection
from elasticsearch import helpers
from app.tools.jsonUtils import response_json
import datetime
elk = Blueprint("elk", __name__)


@elk.route('/nginx_status_code_count')
def status_code_count():
    """
    获取nginx的所有状态码 并统计对应的次数
    :return: like: {"200":1345, "404":103, "502":12}
    """
    count_date = datetime.datetime.now().strftime('%Y.%m.%d')
    es = init_es_connection()
    status_res = {}
    _index = "nginx-accesslog-2017.10.16".format(count_date)
    _body = {"query": {"match_all": {}},
             "sort": [{"@timestamp": 'desc'}],
             "size": 200}
    scanresp = helpers.scan(es, _body, scroll="10m", index=_index, timeout="10m")
    for resp in scanresp:
        try:
            staus_code = resp['_source']['status']
        except Exception,e:
            continue
        if status_res.has_key(staus_code):
            try:
                status_res[resp['_source']['status']] += 1
            except Exception, e:
                continue
        else:
            status_res[resp['_source']['status']] = 1
    return response_json(200, '', status_res)


@elk.route('/nginx_pv_count')
def nginx_pv_count():
    """
    每个项目的pv统计
    :return:
    """
    count_date = datetime.datetime.now().strftime('%Y.%m.%d')
    es = init_es_connection()
    pv_res = {}
    _index = "nginx-accesslog-2017.10.16".format(count_date)
    _body = {"query": {"match_all": {}},
             "sort": [{"@timestamp": 'desc'}],
             "size": 200}
    scanresp = helpers.scan(es, _body, scroll="10m", index=_index, timeout="10m")
    for resp in scanresp:
        try:
            url_split = resp['_source']['request'].split()[1].split("/")
        except Exception,e:
            continue
        product_name = url_split[1].split('?')[0] if url_split[1] else "/"
        if pv_res.has_key(product_name):
            pv_res[product_name] += 1
        else:
            pv_res[product_name] = 1
        pv_res = dict(sorted(pv_res.items(), key=lambda d: d[1], reverse=True)[0:10:])
    return response_json(200, '', pv_res)
