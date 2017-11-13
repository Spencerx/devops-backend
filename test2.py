#!/usr/bin/env python
# -*- coding: utf-8 -*-
import docker

client = docker.DockerClient(base_url='tcp://171.221.199.201:2375', version='1.24')

print client.images.list()