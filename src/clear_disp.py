#!/usr/bin/env python3
"""
File: clear_disp.py
Author: itsf4llofstarts
Description: Clears and sleeps the display
"""
import logging
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# import time
# import traceback


picdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "pic"
)
libdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib"
)

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in2

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd4in2.EPD()

    epd.init()
    epd.Clear()
    epd.sleep()
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()

sys.exit()
