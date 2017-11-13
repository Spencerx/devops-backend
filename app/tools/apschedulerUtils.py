#!/usr/bin/env python
# -*- coding: utf-8 -*-


from apscheduler.triggers.cron import CronTrigger


def evaluate(expression):
    """
    order of values
    year, month, day, week, day_of_week, hour, minute, second, start_date, end_date, timezone
    :param expression:
    :return:
    """

    splitvalues = expression.split()
    for i in range(0, 8):
        if i == 0:
            if splitvalues[0] == '?':
                year = None
            else:
                year = splitvalues[0]
        if i == 1:
            if splitvalues[1] == '?':
                month = None
            else:
                month = splitvalues[1]
        if i == 2:
            if splitvalues[2] == '?':
                day = None
            else:
                day = splitvalues[2]
        if i == 3:
            if splitvalues[3] == '?':
                week = None
            else:
                week = splitvalues[3]
        if i == 4:
            if splitvalues[4] == '?':
                day_of_week = None
            else:
                day_of_week = splitvalues[4]
        if i == 5:
            if splitvalues[5] == '?':
                hour = None
            else:
                hour = splitvalues[5];
        if i == 6:
            if splitvalues[6] == '?':
                minute = None
            else:
                minute = splitvalues[6]
        if i == 7:
            if splitvalues[7] == '?':
                second = None
            else:
                second = splitvalues[7]
    return year, month, day, week, day_of_week, hour, minute, second


def get_trigger(cron_expression):
    """
    生成cron字典
    :param cron_expression:
    :return:
    """
    year, month, day, week,  day_of_week, hour, minute, second = evaluate(cron_expression)
    trigger = CronTrigger(year, month, day, week, day_of_week, hour, minute, second)
    var = [item for item in trigger.fields]
    key = ["year", "month", "day", "week", "day_of_week", "hour", "minute", "second"]
    return dict(zip(key, var))


