#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectTimeout,ProxyError,ConnectionError,ReadTimeout
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
r = requests.get('http://www.xicidaili.com/wt/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
for idx, tr in enumerate(soup.find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        ip = str(tds[1].text)
        port = int(tds[2].text)
        try:
            r = requests.get('http://members.3322.org/dyndns/getip', proxies={'http': '{0}:{1}'.format(ip, port)}, timeout=5)
            print r.status_code
            print '{0} {1}'.format(ip, port)
        except ConnectTimeout, _:
            pass
        except ProxyError, _:
            pass
        except ConnectionError, _:
            pass
        except ReadTimeout, _:
            pass