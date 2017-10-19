#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import base64
from flask import current_app
from app.tools.jsonUtils import response_json
from requests.exceptions import Timeout
from urlparse import urljoin


def registed_service(scope="", service=""):
    """
    :param scope: 指定获取backend范围 all:所有服务
    :param service: 当scope不为all时 service来指定获取指定服务的backend信息
    :return:
    """
    ret = {}
    try:
        r = requests.get(urljoin(current_app.config['CONSUL_BASE_URL'], "?recurse"), timeout=12)
    except Timeout, e:
        current_app.logger.error("query upstream backend timeout from consul http api, message:{0}".format(e))
        return response_json(503, "time out", "")
    else:
        all_service = r.json()
        if all_service:
            if scope == "all":
                for s in all_service:
                    backend_attribute = s['Value']
                    per_upstream = s['Key'].split('/')
                    service_name = per_upstream[1]
                    ip = per_upstream[2].split(':')[0]
                    port = per_upstream[2].split(':')[1]
                    ret.setdefault(service_name, []).append({"ip": ip, "port": port,
                                                             "attribute": eval(base64.b64decode(backend_attribute))
                                                             })
            else:
                for s in all_service:
                    per_upstream = s['Key'].split('/')
                    service_name = per_upstream[1]
                    if service_name == service:
                        backend_attribute = s['Value']
                        ip = per_upstream[2].split(':')[0]
                        port = per_upstream[2].split(':')[1]
                        ret.setdefault(service_name, []).append({"ip": ip, "port": port,
                                                                 "attribute": eval(base64.b64decode(backend_attribute))}
                                                                )
            return ret
        else:
            return {}



