#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

r =requests.get("http://192.168.15.255:2379/v2/keys/registry/services/specs/default")

services = r.json()['node']
for i in  services['nodes']:
    service_url = i['key']
    s = requests.get("http://192.168.15.255:2379/v2/keys"+service_url)
    s1 = s.json()
    try:
        extern_flag = eval(s1['node']['value'])['metadata']['labels']['extern']
        if extern_flag=='true':
            print eval(s1['node']['value'])
    except Exception,e:
        pass