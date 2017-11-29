#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

url = 'http://jenkins.highso.com.cn:8073/'
j = Jenkins(url, username='admin', password='Haixue20161116$#@')

print j.version
print j['haixue-w0-crm-bi-web'].url
print j['haixue-prod-course'].get_revision_dict()

