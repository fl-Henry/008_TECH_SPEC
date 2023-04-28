import os
import sys
import random
import asyncio
import aiohttp
import aiofiles
import argparse
import requests

# from aiohttp_socks import ChainProxyConnector, ProxyConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep

# Custom imports
import tests

from general_methods import DaNHandler, arg_parser, dates_between, delete_last_print_lines, url_to_name
from print_tags import Tags


# # ===== General Variables =================================================================== General Variables =====
...
# # ===== General Variables =================================================================== General Variables =====


# Parsing the arguments
args = arg_parser()
dan = DaNHandler()

ua = UserAgent()
HEADERS = {
        'User-Agent': ua.random,
        'X-Requested-With': 'XMLHttpRequest'
    }


# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


async def write_file(session, file_url, file_path, stdout_key=False):
    async with session.get(file_url, timeout=10) as response:
        try:
            content = await response.read()
            resp_text = await response.text()

            if resp_text == "Not Found [CFN #0005]":
                print(f"{Tags.Red}File doesn't exist:{Tags.ResetAll} {file_url}")
            else:
                async with aiofiles.open(file_path, mode='wb') as f:
                    await f.write(content)
                if stdout_key:
                    print(f'{Tags.Yellow}File is downloaded:{Tags.ResetAll} {file_url}')
                    print(f'               Dir: {file_path}')
        except UnicodeDecodeError as _ex:
            resp_text = await response.text(encoding="latin-1")
            if resp_text == "Not Found [CFN #0005]":
                print(f"{Tags.Red}File doesn't exist:{Tags.ResetAll} {file_url}")
            else:
                async with aiofiles.open(file_path, mode='wb') as f:
                    await f.write(content)
                if stdout_key:
                    print(f'{Tags.Yellow}File is downloaded:{Tags.ResetAll} {file_url}')
                    print(f'               Dir: {file_path}')


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def url_generator(date_: tuple[int, int, int], der):
    """

    :param date_: tuple[int, int, int]     | (31, 12, 2023)
    :param der: str                        | str from list values_for_url[...]
    :return:
    """
    dd, mm, yyyy = date_
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


async def check_file_if_exists(session, date_item, der):


    retry_options = ExponentialRetry(attempts=5)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(file_url) as response:
        resp_text = await response.text()
        if resp_text != "Not Found [CFN #0005]":
            return file_url
        else:
            return None


def get_files_urls(star_date, end_date, values_for_url):
    # Getting all dates between star_date and end_date
    dates_list = dates_between(star_date, end_date)

    # Creating blank dict for every key
    file_url_dict = {}
    for key in values_for_url.keys():
        file_url_dict.update({key: {}})

    # Creating blank list for every der
    for key in values_for_url.keys():
        for der in values_for_url[key]:
            file_url_dict[key].update({der: []})

    # Generating urls of files
    for date_item in dates_list:
        for key in values_for_url.keys():
            for der in values_for_url[key]:
                file_url = url_generator(date_item, der)
                file_url_dict[key][der].append(file_url)

    return file_url_dict


async def save_reports(files_urls):

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = []
        for key in files_urls.keys():
            file_dir = f"{dan.dirs[key]}"
            for der in files_urls[key]:
                for file_url in files_urls[key][der]:
                    file_date = url_to_name(file_url, iter_count=2)
                    file_name = url_to_name(file_url)
                    file_path = f"{file_dir}{file_date}_{file_name}"
                    task = asyncio.create_task(write_file(session, file_url, file_path, stdout_key=True))
                    tasks.append(task)

        await asyncio.gather(*tasks)

    # for file_url in files_urls[]:
        #         image_name = f'{url_to_name(image_url)}'
        #         task = asyncio.create_task(write_file(session, image_url, image_name))
        #         tasks.append(task)
        #     await asyncio.gather(*tasks)


def start_app():
    start_time = datetime.now()

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

    # Creating urls of files
    files_urls = get_files_urls(
        star_date=args['start_date'],
        end_date=args['end_date'],
        values_for_url=values_for_url
    )

    # Save file to temporary folder
    asyncio.run(save_reports(files_urls))

    ...
    ...
    # Stdout working time
    end_time = datetime.now()
    work_time = end_time - start_time
    print("Working time of the app:", work_time)


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    start_app()

