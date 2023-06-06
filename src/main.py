#!/usr/bin/env python3
"""
File: main.py
Author: itsf4llofstarts
Description: Weather text and ascii displayd on e-paper
"""
import logging
import os
import re
import sys
# import time
# import traceback

# from PIL import Image, ImageDraw, ImageFont

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


def get_metar(filename) -> str:
    metar = ""
    try:
        with open(filename) as read:
            metars = read.readlines()
    except FileNotFoundError as fnfe:
        print(f"{fnfe}")
    else:
        metar = metars[-1].strip()
    finally:
        if metar is not None:
            return metar


def get_station(metar):
    return metar[:4]


def get_day_time(metar):
    """KALN 052023Z """
    return metar[5:12]


def get_winds(metar):
    winds = re.compile(r"\s\d{5}(G\d{2})?KT\s")
    wind_dir_sp = re.search(winds, metar)
    return wind_dir_sp.group().strip()


def parse_wind(winds_str):
    dir = winds_str[0:3]
    speed = winds_str[3:5]
    if "G" in winds_str:
        return int(dir), int(speed), True
    return int(dir), int(speed), False


def main():
    metar_file = os.path.expanduser(os.path.join("~", "python", "metar_parser", "metar.txt"))
    # curr_metar = get_metar(metar_file)
    curr_metar = "060050Z 28016G23KT 10SM CLR 24/08 A2999"
    station = get_station(curr_metar)
    day_time = get_day_time(curr_metar)
    winds = get_winds(curr_metar)
    wind_dir, wind_sp, gusty = parse_wind(winds)

    # KALN 060050Z 37013KT 10SM CLR 24/08 A2999
    # KALN 060050Z 19017G24KT 10SM CLR 24/08 A2999

    print(f"{station}")
    print(f"{curr_metar}")
    print(f"{day_time}")
    print(f"{winds}")
    print(f"{wind_dir} {wind_sp} {gusty}")

    epd = epd4in2.EPD()
    if len(sys.argv) == 2 and sys.argv[1] == "-c":
        epd.init()
        epd.Clear()
        epd.sleep()
        sys.exit()
    """
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
        """


if __name__ == "__main__":
    sys.exit(main())
