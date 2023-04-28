import os
import sys
import random
import argparse
import requests

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import sleep

# Custom imports
import tests

from general_methods import DaNHandler, arg_parser


# # ===== General Variables =================================================================== General Variables =====
...
# # ===== General Variables =================================================================== General Variables =====


# Parsing the arguments
args = arg_parser()
dan = DaNHandler()


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def url_generator(dd, mm, yyyy, der):
    """

    :param dd: int              | day
    :param mm: int              | month
    :param yyyy: int            | year
    :param der: str             | str from list values_for_url[...]
    :return:
    """
    base_url = "http://tsjdgo.gob.mx/Recursos"
    if (dd <= 31) and (mm <= 12) and (yyyy >= 2017):
        if (mm <= 9) and (yyyy == 2017):
            if (mm == 9) and (dd > 26):
                url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}pdf"
            else:
                url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}swf"
        else:
            url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}pdf"
    else:
        url = f"{base_url}/images/flash/ListasAcuerdos/{dd}{mm}{yyyy}/{der}swf"
    return url


def scrape_values_for_urls():
    urls = [
        "http://tsjdgo.gob.mx/Recursos/ListasDeAcuerdos.html#",
    ]
    css_selectors = {
        8: "#panel-oculto input.der",    # radio_buttons for De la capital
        9: "#panel-oculto2 input.der",   # radio_buttons for Gómez Palacio y Lerdo
        10: "#panel-oculto1 input.der",  # radio_buttons for Juzgados foraneos
    }

    response = requests.get(urls[0])
    soup = BeautifulSoup(response.text, "lxml")
    list_capital = soup.select(css_selectors[8])
    list_lerdo = soup.select(css_selectors[9])
    list_foraneos = soup.select(css_selectors[10])
    values_for_url = {
        "capital": [x['value'] for x in list_capital],
        "lerdo": [x['value'] for x in list_lerdo],
        "foraneos": [x['value'] for x in list_foraneos],
    }

    return values_for_url


def start_app():

    print(args["stdout"])
    print(dan)

    # URLs and selectors used in the application
    urls = [
        "http://tsjdgo.gob.mx/Recursos/ListasDeAcuerdos.html#",
    ]
    css_selectors = {
        1: "#contenedor1",                   # button with text De la capital
        2: "#contenedor2",                   # button with text Gómez Palacio y Lerdo
        3: "#contenedor3",                   # button with text Juzgados foraneos
        4: "#panel-oculto",                  # block after clicking button with text De la capital
        5: "#panel-oculto2",                 # block after clicking button with text Gómez Palacio y Lerdo
        6: "#panel-oculto1",                 # block after clicking button with text Juzgados foraneos
        7: "input.der",                      # radio_buttons
        8: "#panel-oculto input.der",        # radio_buttons for De la capital
        9: "#panel-oculto2 input.der",       # radio_buttons for Gómez Palacio y Lerdo
        10: "#panel-oculto1 input.der",      # radio_buttons for Juzgados foraneos
    }

    # Getting values for url_generator
    values_for_url = scrape_values_for_urls()

    # Test of url_generator
    tests.tests_url_generator(values_for_url)


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    start_app()

