#!/usr/bin/python

import os
import aiohttp
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_IP = os.environ.get('BASE_IP', '192.168.1')
RANGE_FROM = int(os.environ.get('RANGE_FROM', '1'))
RANGE_TO = int(os.environ.get('RANGE_TO', '255'))
TIMEOUT = float(os.environ.get('TIMEOUT', '30'))
REQUEST_URL = os.environ.get('REQUEST_URL', '/cm?cmnd=status%200')
DEV = os.environ.get('DEV', 'false')

CLIENT_TIMEOUT = aiohttp.ClientTimeout(TIMEOUT)