import logging
import os
import requests
import sys
import config
import math

from PIL import ImageFont
from pathlib import Path

from pycoingecko import CoinGeckoAPI

logger = logging.getLogger("UTILS")


class ScanError(Exception):
    pass


def check_epd_size():
    """Check EPD_SIZE is defined
    """
    if os.path.exists("/etc/default/epd-fuse"):
        exec(open("/etc/default/epd-fuse").read(), globals())

    if EPD_SIZE == 0.0:
        print("Please select your screen size by running 'papirus-config'.")
        sys.exit()


def create_font(font, size):
    """Create fonts from resources
    """
    # Construct paths to foder with fonts
    pathfreemono = Path.cwd().joinpath("resources", "fonts", "FreeMono.ttf")
    pathfreemonobold = Path.cwd().joinpath("resources", "fonts", "FreeMonoBold.ttf")
    pathsawasdee = Path.cwd().joinpath("resources", "fonts", "Sawasdee-Bold.ttf")

    if font == "freemono":
        return ImageFont.truetype(pathfreemono.as_posix(), size)
    if font == "freemonobold":
        return ImageFont.truetype(pathfreemonobold.as_posix(), size)
    if font == "sawasdee":
        return ImageFont.truetype(pathsawasdee.as_posix(), size)
    else:
        print("Font not available")


def get_btc_price(fiat_code):
    """Get BTC -> FIAT conversion
    """
    # TODO Remove dependency for CoinGeckoAPI - simple get call with requests
    price = CoinGeckoAPI().get_price(ids="bitcoin", vs_currencies=fiat_code)
    return price["bitcoin"][fiat_code]


def get_sats():
    return config.FIAT * 100 * config.SATPRICE


def get_sats_with_fee():
    return math.floor(config.SATS * (float(config.conf["atm"]["fee"]) / 100))
