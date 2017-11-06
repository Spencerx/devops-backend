#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from app.tools.jsonUtils import response_json
from app.tools.connectpoolUtils import create_consul_connection


def registed_service(scope="", service=""):
    """
    :param scope: 指定获取backend范围 all:所有服务
    :param service: 当scope不为all时 service来指定获取指定服务的backend信息
    :return:
    """
    try:
        c = create_consul_connection()
        res = c.kv.get('', keys=True, recurse=True)[1]
    except Exception, e:
        current_app.logger.error("query upstream backend timeout from consul , message:{0}".format(e))
        return response_json(503, "consul service error", "")
    ret = {}
    if res:
        if scope == 'all':
            for ups in res:
                ip = ups.split('/')[2].split(':')[0]
                port = ups.split('/')[2].split(':')[1]
                attr = c.kv.get(key=ups, recurse=True)[1][0]['Value']
                ret.setdefault(ups.split('/')[1], []).append({"ip": ip, "port": port,
                                                              "attribute": eval(attr)})
        else:
            for ups in res:
                svc = ups.split('/')[1]
                if svc == service:
                    ip = ups.split('/')[2].split(':')[0]
                    port = ups.split('/')[2].split(':')[1]
                    attr = c.kv.get(key=ups, recurse=True)[1][0]['Value']
                    ret.setdefault(ups.split('/')[1], []).append({"ip": ip, "port": port,
                                                                  "attribute": eval(attr)})
    return ret





