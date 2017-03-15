#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import fibo_app
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = "fibo.log"
LOG_MAX_SIZE = 1024*1024*10
LOG_FILE_NUM = 3

handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=LOG_MAX_SIZE, backupCount=LOG_FILE_NUM)
logger = logging.getLogger('werkzeug')
logger.addHandler(handler)

fibo_app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8888)))