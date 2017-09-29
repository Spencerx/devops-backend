#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import Redis
from os.path import join,isfile
from os import listdir
from gevent import monkey
import gevent
monkey.patch_all()
import os


def delete_dump_keys_v2(dump):
    ip = dump.split("-")[0].strip()
    port = int(dump.split("-")[1].strip())
    r = Redis(host=ip, port=port)
    with open("dump_files_2/"+dump) as f:
        for line in f.readlines():
            if line.strip():
                line = line.strip()
                os.system("redis-cli -h {0} -p {1} del {2}".format(ip, port, line))


if __name__ == '__main__':
    all_dump_files = [f for f in listdir('dump_files/') if isfile(join('dump_files/', f))]
    task = []
    for i in all_dump_files:
        delete_dump_keys_v2(i)

gevent.joinall(task)


