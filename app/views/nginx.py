#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import pprint

es = Elasticsearch(hosts='192.168.15.255', port=9200)


# res = es.search(index="k8s-nginx-access-2017.10.15", body={"query": {"wildcard": {"domain": "*k8s*"}},
#                                                           "sort": [{"@timestamp": 'desc'}]})
res = es.search(index="k8s-nginx-access-2017.10.15", body={"query": {"match_all": {}},
                                                           "sort": [{"@timestamp": 'desc'}], "size": 200})
count = 0
status_res = {}
print len(res['hits']['hits'])
for i in res['hits']['hits']:
    # print i['_source']['status']
    if status_res.has_key(i['_source']['status']):
        status_res[i['_source']['status']] += 1
    else:
        status_res[i['_source']['status']] = 1
print status_res

s = '/ss'
s2 = '/sss/'
s3 = '/'
print s.split("/")
print s2.split("/")
print s3.split("/")

a = {"apple":10, "mac":8, "and": 80, "wp":6}
sorted_x = sorted(a.iteritems(), key=lambda x: x[1], reverse=True)

print dict(sorted_x)