#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import Redis
from os import listdir
from os.path import isfile, join
import datetime
from rediscluster import StrictRedisCluster

cluster_nodes = [
        {'host': '192.168.1.201', 'port': 6008},
        {'host': '192.168.1.73', 'port': 6009},
        {'host': '192.168.1.69', 'port': 6008},
        {'host': '192.168.1.73', 'port': 6008}
    ]

# 11.84 G
# 8.25 G
# 7.12 G
# 8.58 G

# 5.49 G
# 1.02 G
# 666.41 M
# 1.02 G


def dump_redis_cluster_keys():
    pattens = ['e:USER_OUTLINE_CAPACITY_VALUE*', 'e:USER_QUESTION_CAPACITY_VALUE*',
               'e:USER_LAST_DO_QUESTION_WRONG*', 'e:USER_DO_QUESTION_WRONG_COUNT*',
               'e:USER_DO_ANSWER_QUESTION_COUNT*', 'e:USER_DO_QUESTION_COUNT*'
               ]
    count = 0
    for node in cluster_nodes:
        r = Redis(host=node['host'], port=node['port'])
        for patten in pattens:
            result = r.keys(patten)
            with open("dump_files/" + str(node['host']) + '-' + str(node['port']) + '-' + patten + '.txt', 'a+') as f:
                for res in result:
                    f.write(res+'\n')
                    count += 1
        print node['host'] + "  " + str(node['port']) + ' dump ' + str(count) + ' keys'
        count = 0


def delete_dump_keys():
    all_dump_files = [f for f in listdir('dump_files/') if isfile(join('dump_files/', f))]
    print all_dump_files
    for dump in all_dump_files:
        with open("dump_files/"+dump) as f:
            for line in f.readlines():
                if line.strip():
                    r = StrictRedisCluster(startup_nodes=cluster_nodes)
                    line = line.strip()
                    r.delete(line)


def delete_dump_keys_v2():
    all_dump_files = [f for f in listdir('dump_files/') if isfile(join('dump_files/', f))]
    for dump in all_dump_files:
        ip = dump.split("-")[0].strip()
        port = int(dump.split("-")[1].strip())
        r = Redis(host=ip, port=port)
        with open("dump_files/"+dump) as f:
            for line in f.readlines():
                if line.strip():
                    line = line.strip()
                    print line
                    r.delete(line)



if __name__ == '__main__':
    print "================"
    print "dump key start ..."
    start = datetime.datetime.now()
    dump_redis_cluster_keys()
    end = datetime.datetime.now()
    print "dump key finish ..."
    print "dump key use {0} ".format(end-start)
    print "================"

    start = datetime.datetime.now()
    print "delete key start..."
    # delete_dump_keys()
    end = datetime.datetime.now()
    print "delete key finish..."
    print "delete key use {0} ".format(end - start)

