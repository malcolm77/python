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
import requests

logging.basicConfig(level=logging.INFO)

def get_gpu():
  url = requests.get("http://mcpc:9835/metrics")
  for line in url.text.splitlines():
    if "nvidia_smi_utilization_gpu_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
      try:
        gpu = float(line[-4:])*100
        # print(str(gpu) + "%" )
      except:
        gpu = 0
  return str(gpu)

try:
    # setup
    epd = epd2in13_V3.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # define fonts
    # font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    myfont = ImageFont.truetype('/usr/local/share/fonts/Font.ttc', 48)

    # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    epd.displayPartBaseImage(epd.getbuffer(time_image))
    num = 0
    while (True):
        time_draw.rectangle((12, 8, 220, 105), fill = 255)
        time_draw.text((12, 8), get_gpu(), font = myfont, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        # if(num == 10000):
        #    break 
    
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit(cleanup=True)
    exit()

# import urllib.request
# page = urllib.request.urlopen('http://owlbear:9100/metrics')
# print(page.read())

import requests
url = requests.get("http://mcpc:9835/metrics")
for line in url.text.splitlines():
    # print(line)
    # if line == "node_nfsd_connections_total 3":
    # if "node_hwmon_temp_celsius{chip=\"acpitz\",sensor=\"temp1\"} " in line:
    if "nvidia_smi_utilization_gpu_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
      gpu = float(line[-4:])*100
      print(str(gpu) + "%" )
