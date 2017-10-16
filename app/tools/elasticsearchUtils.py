#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import os

env = os.environ.get('ads_env', 'dev')
if env == 'prod':
    from ..private_config import ProdConfig as Config
else:
    from ..private_config import DevConfig as Config


def init_es_connection():
    """
    es init connection
    :return:es connection
    """
    es = Elasticsearch(hosts=Config.ES['host'], port=Config.ES['port'])
    return es
