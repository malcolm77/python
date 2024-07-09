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

font_height = 48

def get_gpu_info():
  gpu_info = []
  try:
    url = requests.get("http://mcpc:9835/metrics",timeout=5)
    for line in url.text.splitlines():
      if "nvidia_smi_utilization_gpu_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gpu = int(line[-2:])
        except:
          gpu = 0
      elif "nvidia_smi_temperature_gpu{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gtemp = int(line[-2:])
        except:
          gtemp = 0
      elif "nvidia_smi_fan_speed_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gfan = int(line[-2:])
        except:
          gfan = 0
      gpu_info = [gpu,gtemp,gfan]
  except:
    gpu = -1
    gtemp = -1
    gfan = -1
  return gpu_info

def get_gpu():
  try:
    url = requests.get("http://mcpc:9835/metrics",timeout=5)
    for line in url.text.splitlines():
      if "nvidia_smi_utilization_gpu_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        # print(line)
        try:
          gpu = int(line[-2:])
          # print(str(gpu) + "%" )
        except:
          gpu = 0
  except:
    gpu = 0
  return str(gpu) + " %"

def get_gtemp():
  try:
    url = requests.get("http://mcpc:9835/metrics",timeout=5)
    for line in url.text.splitlines():
      if "nvidia_smi_temperature_gpu{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          # print(line)
          gtemp = int(line[-2:])
        except:
          gtemp = 0
  except:
    gtemp = 0
  return str(gtemp) + " C"

def get_gfan():
  try:
    url = requests.get("http://mcpc:9835/metrics",timeout=5)
    for line in url.text.splitlines():
      if "nvidia_smi_fan_speed_ratio{uuid=\"72f02a28-5140-325e-ba49-1ae77c6b4e30\"}" in line:
        try:
          gtemp = int(line[-2:])
        except:
          gtemp = 0
  except:
    gtemp = 0
  return str(gtemp) + " %"

def cleanup():
  epd.init()
  epd.Clear(0xFF)
  epd.sleep()
  epd2in13_V3.epdconfig.module_exit(cleanup=True)


try:
    # setup
    epd = epd2in13_V3.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    logging.info("height:"+str(epd.height))
    logging.info("width:"+str(epd.width))

    # define fonts
    myfont = ImageFont.truetype('/usr/local/share/fonts/Font.ttc', font_height)
    smallfont = ImageFont.truetype('/usr/local/share/fonts/Font.ttc', 12)

    # partial update
    logging.info("Getting GPU info...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    epd.displayPartBaseImage(epd.getbuffer(time_image))
    num = 0
    while (True):
        # time_draw.rectangle((12, 8, 220, 105), fill = 255)
        time_draw.rectangle((0, 0, 250, 122), fill = 255)

        time_draw.text((12,0), "GPU usage", font = smallfont, fill = 0)
        time_draw.text((12, 8), get_gpu(), font = myfont, fill = 0)

        time_draw.text((12,font_height+font_height+12), "GPU Temp", font = smallfont, fill = 0)
        time_draw.text((12, 8+font_height), get_gtemp(), font = myfont, fill = 0)

        time_draw.text((130,0), "FAN Speed", font = smallfont, fill = 0)
        time_draw.text((130, 8), get_gfan(), font = myfont, fill = 0)

        time_draw.text((130, 8+font_height), time.strftime('%I:%M'), font = myfont, fill = 0)

        epd.displayPartial(epd.getbuffer(time_image))
        time.sleep(10)
    
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    # epd2in13_V3.epdconfig.module_exit(cleanup=True)
    cleanup()
    exit()
