#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *


def last_week_date():
    """
    计算上周周一和周五的日期
    :return: [last_monday, last_friday]
    """
    now = datetime.now()
    last_fri = now + relativedelta(weekday=FR(-1))
    last_mon = last_fri + relativedelta(weekday=MO(-1))
    last_tu = last_mon + timedelta(days=1)
    last_th = last_tu + timedelta(days=1)
    last_we = last_th + timedelta(days=1)
    last_sat = last_fri + timedelta(days=1)
    return [last_mon.strftime('%Y-%m-%d'),
            last_tu.strftime('%Y-%m-%d'),
            last_th.strftime('%Y-%m-%d'),
            last_we.strftime('%Y-%m-%d'),
            last_fri.strftime('%Y-%m-%d'),
            last_sat.strftime('%Y-%m-%d')]
