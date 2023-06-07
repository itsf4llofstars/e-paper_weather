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


def main():
    try:
        epd = epd4in2.EPD()

        epd.init()
        epd.Clear()
        if len(sys.argv) == 2 and sys.argv[1] == "-c":
            epd.sleep()
            sys.exit()

        font18 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 18)
        font20 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 20)
        font22 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 22)
        font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 24)
        font36 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 36)

        lat = "48.20.09"
        lon = "122.39.07"
        iss = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(iss)
        draw.text((10, 0), "ISS", font=font36, fill=0)
        draw.text((10, 40), "Latitude / Longitude", font=font36, fill=0)
        draw.text((10, 80), f"{lat}, {lon}", font=font36, fill=0)
        epd.display(epd.getbuffer(iss))

        # epd.Clear()
        epd.sleep()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()


if __name__ == "__main__":
    sys.exit(main())
