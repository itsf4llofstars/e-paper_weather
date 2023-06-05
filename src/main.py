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
        epd = epd4in2.EPD()

        if len(sys.argv) == 2 and sys.argv[1] == "-c":
            epd.init()
            epd.Clear()
            epd.sleep()
            sys.exit()

        epd.init()
        epd.Clear()

        font18 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 18)
        font20 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 20)
        font22 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 22)
        font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 24)
        font36 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 36)

        # Draw the METAR weather
        # KALN 051950Z 03009KT 10SM CLR 28/05 A3001
        metar_wx = Image.new("1", (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(metar_wx)
        draw.text((10, 0), "KALN", font=font36, fill=0)
        draw.text((10, 40), "051950Z 03009KT 10SM CLR 28/05 A3001", font=font18, fill=0)
        draw.text((10, 65), "Date / Time: June 5, 1450LCL", font=font18, fill=0)
        draw.text((10, 90), "Winds: NE at 9KTS", font=font22, fill=0)
        draw.text((10, 115), "Vis: 10SM", font=font22, fill=0)
        draw.text((10, 140), "Sky: CLEAR", font=font22, fill=0)
        draw.text((10, 165), "Temp: 28C - 86F", font=font22, fill=0)
        draw.text((10, 190), "Baro: 30.02 in/Hg", font=font22, fill=0)
        draw.text((10, 215), "xxx\nxxx", font=font18, fill=0)
        epd.display(epd.getbuffer(metar_wx))
        time.sleep(5)

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
