#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
from conf.config import logs

# Create object to write logs
logger = logging.getLogger()

# Logs level
logger.setLevel(eval('{0}.{1}'.format('logging', logs['level'])))

# Create formatter to get time and level msg
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

# Create handler to redirect logs to file (max size: 1M)
file_handler = RotatingFileHandler(
    os.path.join(logs['path'], 'awsome-uploader.log'), 'a', 1000000, 1)

# Set loglevel to handler
file_handler.setLevel(eval('{0}.{1}'.format('logging', logs['level'])))

# Add handler with formatter to logger
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create another handler to redirect logs to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(eval('{0}.{1}'.format('logging', logs['level'])))
logger.addHandler(stream_handler)
