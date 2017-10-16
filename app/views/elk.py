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
    _index = "k8s-nginx-access-{0}".format(count_date)
    _body = {"query": {"match_all": {}},
             "sort": [{"@timestamp": 'desc'}],
             "size": 200}
    scanresp = helpers.scan(es, _body, scroll="10m", index=_index, timeout="10m")
    for resp in scanresp:
        if status_res.has_key(resp['_source']['status']):
            status_res[resp['_source']['status']] += 1
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
    _index = "k8s-nginx-access-{0}".format(count_date)
    _body = {"query": {"match_all": {}},
             "sort": [{"@timestamp": 'desc'}],
             "size": 200}
    scanresp = helpers.scan(es, _body, scroll="10m", index=_index, timeout="10m")
    for resp in scanresp:
        print resp
        url_split = resp['_source']['request'].split()[1].split("/")
        product_name = url_split[1] if url_split[1] else "/"
        if pv_res.has_key(product_name):
            pv_res[product_name] += 1
        else:
            pv_res[product_name] = 1
    return response_json(200, '', pv_res)
