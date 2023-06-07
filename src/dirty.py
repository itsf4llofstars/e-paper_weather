#!/usr/bin/env python3
"""
File: main.py
Author: itsf4llofstarts
Version: 0.1.0
Release: 1
Description: Weather text and ascii displayd on e-paper
"""
import logging
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

# import time
# import traceback

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
    return re.search(r"^K\w{3}\s", metar).group().strip()


def get_day_time(metar):
    day_zulu = re.search(r"\s\d{6}Z\s", metar).group().strip()
    return day_zulu[:2], day_zulu[2:6]


def get_winds(metar):
    winds = ""
    if "VRB" in metar:
        winds = re.search(r"\sVRB\d{2}KT\s", metar)
    winds = re.search(r"\s\d{5}(G\d{2})?KT\s", metar).group().strip()
    return winds[:3], winds[3:5]


def get_vis(metar):
    return re.search(r"\s[0-9]?[0-9]SM\s", metar).group().strip()[:-2]


def get_sky(metar):
    if "CLR" in metar:
        return "CLEAR"
    elif "OVC" in metar:
        return "OVERCAST"
    elif "BKN" in metar:
        return "BROKEN"
    elif "SCT" in metar:
        return "SCATTERED"
    else:
        return "NO SKY"


def get_temp(metar):
    temp = re.search(r"\sM?\d{2}\/M?\d{2}\s", metar).group().strip()

    if "M" in temp:
        temp = temp[1:3]
    else:
        temp = temp[:2]

    return int((float(temp) * 1.8) + 32.0)


def get_baro(metar):
    baro = re.search(r"\sA\d{4}$", metar).group().strip()
    return f"{baro[1:3]}.{baro[3:5]} in/Hg"


def main():
    metar_file = os.path.expanduser(
        os.path.join("~", "python", "metar_parser", "metar.txt")
    )
    curr_metar = get_metar(metar_file)
    station = get_station(curr_metar)
    day, time_zulu = get_day_time(curr_metar)
    wind_dir, wind_speed = get_winds(curr_metar)
    visibility = get_vis(curr_metar)
    visibility += " Miles"
    sky_condition = get_sky(curr_metar)
    temp_f = str(get_temp(curr_metar))
    barometer = get_baro(curr_metar)

    clouds = """      .-----.
     (        ).
    (_____)___)
    * * * * *
     * * * * *
"""

    try:
        epd = epd4in2.EPD()

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
        draw.text((10, 0), station, font=font36, fill=0)
        draw.text((10, 50), f"June {day} {time_zulu}Z", font=font20, fill=0)
        draw.text((10, 75), f"{wind_dir} at {wind_speed} KNOTS", font=font20, fill=0)
        draw.text((10, 100), visibility, font=font20, fill=0)
        draw.text((10, 125), sky_condition, font=font20, fill=0)
        draw.text((10, 150), f"{temp_f} F", font=font20, fill=0)
        draw.text((10, 175), barometer, font=font20, fill=0)

        if "RA" in curr_metar:
            draw.text((10, 200), "Rain", font=font20, fill=0)

        # draw.text((10, 150), clouds, font=font22, fill=0)
        epd.display(epd.getbuffer(metar_wx))

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
