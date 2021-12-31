# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

bind = '0.0.0.0:8443'
workers = 1
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
certfile = './certs/targetproject.crt'
keyfile = './certs/targetproject.key'