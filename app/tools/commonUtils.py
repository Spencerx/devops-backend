#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yagmail


def send_email(to_list, subject, content):
    yag = yagmail.SMTP(user='security@haixue.com', password='Haixue20170228', host='smtp.exmail.qq.com', port='465')
    for receiver in to_list:
        yag.send(to=receiver, subject=subject, contents=content)

send_email(['591356683@qq.com'], subject='new app deploy', content='new app will deploy , plz login in cc system to get more about this workflow')


