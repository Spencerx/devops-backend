#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def varify_passwd(password):
    m2 = hashlib.md5()
    src = "123456{1069591}"
    m2.update(src)
    print m2.hexdigest()

varify_passwd(1)