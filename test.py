#!/usr/bin/env python
# -*- coding: utf-8 -*-


#import datetime
#a = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#print type(a)
#
#from xpinyin import Pinyin
#
#p = Pinyin()
#
#print p.get_pinyin(u'孙麒麟','')
#
#from app.models.users import Users
#
#u = Users.select()
#for i in u:
#    if i.can_approved:
#     print i.can_approved
# 导入模块

import requests
#from nginx.config.api import Section,Config,Location
r = requests.get("http://192.168.15.255:8080/api/v1/namespaces/default/services/")
res = r.json()['items']

#events = Section('events', worker_connections='48000')
#http = Section('http', include='mime.types', add_header="service $server_name")

for item in res:
    try:
        if item['metadata']['labels']['extern']:
            service_name = item['metadata']['name']
            service_cluster_ip = item['spec']['clusterIP']
            service_cluster_port = item['spec']['ports'][0]['port']
            print service_name, service_cluster_ip, service_cluster_port
    except KeyError, e:
        pass
#
# nginx = Config(events, http, worker_processes=4, error_log='error.log',)
# with file("nginx.conf", 'w') as f:
#     f.write(str(nginx))

import nginx

import pytz
import datetime
utc_time_str=u"2015-07-31T00:00:00Z"
utc_format='%Y-%m-%dT%H:%M:%SZ'
local_tz = pytz.timezone('Asia/Chongqing')
local_format = "%Y-%m-%d %H:%M"
utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
time_str = local_dt.strftime(local_format)
print time_str




