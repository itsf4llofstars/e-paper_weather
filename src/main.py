#!/usr/bin/env python3
"""
File: main.py
Author: itsf4llofstarts
Description: Weather text and ascii displayd on e-paper
"""
import logging
import os
import sys
import time
import traceback

from PIL import Image, ImageDraw, ImageFont

picdir = ""
libdir = ""

try:
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
except ImportError as ie:
    print(f"{ie}")
    sys.exit()
else:
    print("Imports success")


def main():
    try:
        logging.info("epd4in2 Demo")

        epd = epd4in2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 18)
        font35 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 35)

        # Draw the METAR weather
        metar_wx = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(metar_wx)
        draw.text((10, 0), "hello world", font=font24, fill=0)
        epd.display(epd.getbuffer(metar_wx))
        time.sleep(2)

        epd.Clear()
        epd.sleep()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()


if __name__ == "__main__":
    sys.exit(main())
