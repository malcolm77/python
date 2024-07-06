#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

# logging.basicConfig(level=logging.DEBUG)

epd = epd2in13_V3.EPD()
logging.info("init and Clear")

logging.info("Clear...")
epd.init()
epd.Clear(0xFF)
    
logging.info("Goto Sleep...")
epd.sleep()
    
epd2in13_V3.epdconfig.module_exit(cleanup=True)
