#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from tasks.tasks import week_report

dispatch = Blueprint('dispatch', __name__)


@dispatch.route("/")
def dioadu():
    print ("耗时的任务")
    week_report.delay()
    return u'耗时的任务已经交给了celery'
