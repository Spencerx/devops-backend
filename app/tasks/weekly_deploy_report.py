#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yagmail
from app.models.workflows import Workflow
from app.tools.templateUtils import weekly_report
from app.tools.ormUtils import id_to_service
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import FR, MO, TU, TH


def week_report():
    """
    运维周报task 上周一周上线统计
    :return:
    """
    print 'task start ...'
    d = datetime.now()
    last_monday = (d + relativedelta(weekday=MO(-1))).strftime("%Y-%m-%d 00:00:00")
    last_friday = (d + relativedelta(weekday=TH(-1))).strftime("%Y-%m-%d 00:00:00")
    ws = Workflow().select().where((Workflow.create_time > last_monday)
                                   & (Workflow.close_time < last_friday)
                                   & (Workflow.type == 1))
    ret = {}
    ret['start_date'] = last_monday
    ret['end_date'] = last_friday
    ret.setdefault(ret['services'], {})
    for w in ws:
        if ret['services'].has_key(id_to_service(w.service)):
            ret.setdefault(ret['services'], {})['service']['count'] =1
            if w.status == 4:
                ret['services']['rollback'] = 0
            else:
                ret['services']['rollback'] = 1
        else:
            ret['services']['count'] += 1
            if w.status == 4:
                pass
            else:
                ret['services']['rollback'] += 1


    print weekly_report(ret)
    # yag = yagmail.SMTP('security@haixue.com', 'Haixue20170906', host='smtp.exmail.qq.com', port=465)
    # yag.send(to='591356683@qq.com',
    #          subject='test',
    #          contents='hello,world')

