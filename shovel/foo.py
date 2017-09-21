#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
shovel likes rake in rails, it can help you to execute some task
in my opinion,it may use with gevent to execute some async tasks
example: (curren in devops-backend dictionary) shovel foo.say_name --name Kylin
"""
from shovel import task


@task
def say_name(name):
    print "hello,{0}".format(name)
