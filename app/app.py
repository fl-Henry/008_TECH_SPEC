import os
import sys
import json
import random
import asyncio
import aiohttp
import aiofiles
import argparse
import requests
import cv2 as cv
import numpy as np
import pandas as pd


# sudo apt-get install gnupg
# echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
# sudo apt-get update
# sudo apt-get install -y mongodb-org
# sudo systemctl start mongod
import pymongo

# sudo apt-get install tesseract-ocr
import pytesseract

# sudo apt-get install poppler-utils
from pdf2image import convert_from_path

from aiohttp_retry import RetryClient, ExponentialRetry
from datetime import datetime, timedelta, date

from PIL import Image, PdfImagePlugin
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from json import JSONEncoder
from time import sleep

# Custom imports
import pdf_parser as pp
import general_methods as gm

from print_tags import Tags
from mongodb_handler import MongodbHandler


# # ===== General Variables =================================================================== General Variables =====
...
# # ===== General Variables =================================================================== General Variables =====

...
# Parsing the arguments
args = gm.arg_parser()
dan = gm.DaNHandler()

DB_HOST = "mongodb://db:27017/"
# DB_HOST = "mongodb://127.0.0.1:27017/"

ua = UserAgent()
HEADERS = {
        'User-Agent': ua.random,
        'X-Requested-With': 'XMLHttpRequest'
    }


# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):

    # Override the default method
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


async def write_file(session, file_url, file_path, stdout_key=False):
    """
        # Download and save file
    :param session:
    :param file_url:
    :param file_path:
    :param stdout_key:
    :return:
    """
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


def get_all_files_by_extension(dir_to_find: str, extension: str):
    list_of_pdfs = []
    for inner_dir in os.listdir(dir_to_find):
        for item_file in os.listdir(f"{dir_to_find}{inner_dir}"):
            if item_file[-3:].upper() == extension.upper():
                list_of_pdfs.append(f"{dir_to_find}{inner_dir}/{item_file}")
            else:
                print("File removed:", f"{dan.dirs['temp_dir']}{inner_dir}/{item_file}")
                os.remove(f"{dan.dirs['temp_dir']}{inner_dir}/{item_file}")

    return list_of_pdfs


def dela_to_de_la(proc_str: str):
    """
        fixing wrong recognition of "DE LA" as "DELA"
    :param proc_str:
    :return:
    """
    dela_words = [
        "delacion",
        "delantal",
        "delante",
        "delantera",
        "delantero",
        "delatar",
        "delectatio",
        "delecto",
        "delego",
        "deleo",
    ]
    str_to_return = ""
    last_char_index = 0
    for char_index in range(len(proc_str)):
        str_4char = proc_str[char_index:char_index + 4]
        if str_4char.lower() == "dela":
            match_key = False
            for check_word in dela_words:
                may_be_word = proc_str[char_index:char_index + len(check_word)]
                if may_be_word.lower() == check_word.lower():
                    match_key = True
            if not match_key:
                if proc_str[char_index - 1] == " ":
                    str_to_return += proc_str[last_char_index:char_index] + "DE LA "
                else:
                    str_to_return += proc_str[last_char_index:char_index] + " DE LA "
                last_char_index = char_index + 5
    str_to_return += proc_str[last_char_index:]

    proc_str = str_to_return
    str_to_return = ""
    last_char_index = 0
    for char_index in range(len(proc_str)):
        str_4char = proc_str[char_index:char_index + 4]
        if str_4char.lower() == "delo":
            match_key = False
            for check_word in dela_words:
                may_be_word = proc_str[char_index:char_index + len(check_word)]
                if may_be_word.lower() == check_word.lower():
                    match_key = True
            if not match_key:
                if proc_str[char_index - 1] == " ":
                    str_to_return += proc_str[last_char_index:char_index] + "DE LO "
                else:
                    str_to_return += proc_str[last_char_index:char_index] + " DE LO "
                last_char_index = char_index + 5
    str_to_return += proc_str[last_char_index:]

    return str_to_return


def remove_spec_chars(proc_str: str):
    chars_to_remove = ["_", "=", "|", "\u201c", "\""]
    str_to_return = ""
    for char in proc_str:
        if char not in chars_to_remove:
            str_to_return += char
    return str_to_return


def get_table_words_number(table_df):
    words_counter = 0
    for index, row in table_df.iterrows():
        for item in row:
            words_counter += len(item.split())
    return words_counter


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


class ServerIsDown(Exception):
    def __init__(self):
        super().__init__("Server is down")


def check_date(files_date):

    # Creating rec_index from db
    mdbh = MongodbHandler(host=DB_HOST, db_name="raw", collection_name="juzgados")
    db_rec_indexes = mdbh.collection.find({}, {"_id": 0, "fecha": 1})
    db_rec_indexes = [x["fecha"] for x in db_rec_indexes]

    # Checking if db_rec_index contains files_date
    rec_index = f"{files_date[2]}/{files_date[1]}/{files_date[0]}"
    if rec_index.upper() not in db_rec_indexes:
        mdbh.db_client.close()
        return True

    mdbh.db_client.close()
    return False


def replace_wrong_recognitions(in_str: str):
    replace_dict = {
        "‘TER.": "1ER.",
        "TER.": "1ER.",
        "‘ER.": "1ER.",
        "$": "S",
        "¡": "",
        "»": "",
        "«": "",
        "...": " ...",
        "]": '',
        "(.)": '',
    }
    result_str = in_str
    for key in replace_dict.keys():
        result_str = ""
        last_char = 0
        for char_counter in range(len(in_str) - len(key)):
            if_in = in_str[char_counter:char_counter + len(key)].upper() in [*replace_dict.keys()]
            if if_in:
                result_str += in_str[last_char:char_counter] + replace_dict[key]
                last_char = char_counter + len(key)
        result_str += in_str[last_char:]
        in_str = result_str

    return result_str


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

    # URLs and selectors used in the application
    # urls = [
    #     "http://tsjdgo.gob.mx/Recursos/ListasDeAcuerdos.html#",
    # ]
    # css_selectors = {
    #     1: "#contenedor1",                   # button with text De la capital
    #     2: "#contenedor2",                   # button with text Gómez Palacio y Lerdo
    #     3: "#contenedor3",                   # button with text Juzgados foraneos
    #     4: "#panel-oculto",                  # block after clicking button with text De la capital
    #     5: "#panel-oculto2",                 # block after clicking button with text Gómez Palacio y Lerdo
    #     6: "#panel-oculto1",                 # block after clicking button with text Juzgados foraneos
    #     7: "input.der",                      # radio_buttons
    #     8: "#panel-oculto input.der",        # radio_buttons for De la capital
    #     9: "#panel-oculto2 input.der",       # radio_buttons for Gómez Palacio y Lerdo
    #     10: "#panel-oculto1 input.der",      # radio_buttons for Juzgados foraneos
    # }

    urls = [
        "http://tsjdgo.gob.mx/Recursos/ListasDeAcuerdos.html#",
    ]
    css_selectors = {
        8: "#panel-oculto input.der",    # radio_buttons for De la capital
        9: "#panel-oculto2 input.der",   # radio_buttons for Gómez Palacio y Lerdo
        10: "#panel-oculto1 input.der",  # radio_buttons for Juzgados foraneos
    }

    server_is_down_key = True
    for _ in range(3):
        try:
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
            server_is_down_key = False
            break

        except TimeoutError:
            continue

    if server_is_down_key:
        raise ServerIsDown

    return values_for_url


def get_files_urls(files_date, values_for_url):

    # Creating blank dict for every key
    file_url_dict = {}
    for key in values_for_url.keys():
        file_url_dict.update({key: {}})

    # Creating blank list for every der
    for key in values_for_url.keys():
        for der in values_for_url[key]:
            file_url_dict[key].update({der: []})

    # Generating urls of files
    for key in values_for_url.keys():
        for der in values_for_url[key]:
            file_url = url_generator(files_date, der)
            file_url_dict[key][der].append(file_url)

    return file_url_dict


async def save_reports(files_urls, files_date):

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = []
        for key in files_urls.keys():
            file_dir = f"{dan.dirs[key]}"
            for der in files_urls[key]:
                for file_url in files_urls[key][der]:
                    file_date = f"{files_date[0]}-{files_date[1]}-{files_date[2]}"
                    file_name = gm.url_to_name(file_url)
                    file_path = f"{file_dir}{file_date}_{file_name}"
                    task = asyncio.create_task(write_file(session, file_url, file_path, stdout_key=True))
                    tasks.append(task)

        await asyncio.gather(*tasks)


def add_records_to_db(records_list):
    mdbh = MongodbHandler(host=DB_HOST, db_name="raw", collection_name="juzgados")
    mdbh.collection.insert_many(records_list)
    print(f"{Tags.LightYellow}Saved to db.{Tags.ResetAll}")
    mdbh.db_client.close()


def delete_all_duplicates():
    mdbh = MongodbHandler(host=DB_HOST, db_name="raw", collection_name="juzgados")
    mdbh.delete_duplicates(["actor", "demandado", "juzgado", "expediente", "materia", "fecha"])
    mdbh.db_client.close()


# # ===== Parsing Methods ======================================================================= Parsing Methods =====
...
# # ===== Parsing Methods ======================================================================= Parsing Methods =====


def get_materia(doc_type):
    """"""

    match_dict = {
        "aux1.": "CIVIL",
        "aux2.": "CIVIL",
        "civ2.": "CIVIL",
        "civ3.": "CIVIL",
        "civ4.": "CIVIL",
        "fam1.": "FAMILIAR",
        "fam2.": "FAMILIAR",
        "fam3.": "FAMILIAR",
        "fam4.": "FAMILIAR",
        "fam5.": "FAMILIAR",
        "mer1.": "CIVIL",
        "mer2.": "CIVIL",
        "mer3.": "CIVIL",
        "mer4.": "CIVIL",
        "merOral.": "CIVIL",
        "seccc.": "CIVIL",
        "seccu.": "CIVIL",
        "cjmf1.": "FAMILIAR",
        "cjmf2.": "FAMILIAR",
        "tribl.": "LABORAL",
        "Civ1GP.": "CIVIL",
        "Civ2GP.": "CIVIL",
        "Fam1GP.": "FAMILIAR",
        "Fam2GP.": "FAMILIAR",
        "AuxMixtoGP.": "CIVIL",
        "Fam3GP.": "CIVIL",
        "secccGP.": "CIVIL",
        "seccuGP.": "CIVIL",
        "triblG.": "LABORAL",
        "Mixto1Lerdo.": "CIVIL",
        "Mixto2Lerdo.": "CIVIL",
        "canatlan.": "CIVIL",
        "nombrededios.": "CIVIL",
        "nazas.": "CIVIL",
        "cuencame.": "CIVIL",
        "sanjuandelrio.": "CIVIL",
        "elsalto.": "CIVIL",
        "santamariadeloro.": "CIVIL",
        "victoria.": "CIVIL",
        "santiago.": "CIVIL",
    }

    match_entidad_dict = {
        "aux1.": "DE LA CAPITAL DURANGO",
        "aux2.": "DE LA CAPITAL DURANGO",
        "civ2.": "DE LA CAPITAL DURANGO",
        "civ3.": "DE LA CAPITAL DURANGO",
        "civ4.": "DE LA CAPITAL DURANGO",
        "fam1.": "DE LA CAPITAL DURANGO",
        "fam2.": "DE LA CAPITAL DURANGO",
        "fam3.": "DE LA CAPITAL DURANGO",
        "fam4.": "DE LA CAPITAL DURANGO",
        "fam5.": "DE LA CAPITAL DURANGO",
        "mer1.": "DE LA CAPITAL DURANGO",
        "mer2.": "DE LA CAPITAL DURANGO",
        "mer3.": "DE LA CAPITAL DURANGO",
        "mer4.": "DE LA CAPITAL DURANGO",
        "merOral.": "DE LA CAPITAL DURANGO",
        "seccc.": "DE LA CAPITAL DURANGO",
        "seccu.": "DE LA CAPITAL DURANGO",
        "cjmf1.": "DE LA CAPITAL DURANGO",
        "cjmf2.": "DE LA CAPITAL DURANGO",
        "tribl.": "DE LA CAPITAL DURANGO",
        "Civ1GP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "Civ2GP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "Fam1GP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "Fam2GP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "AuxMixtoGP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "Fam3GP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "secccGP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "seccuGP.": "GOMEZ PALACIO Y LERDO DURANGO",
        "triblG.": "GOMEZ PALACIO Y LERDO DURANGO",
        "Mixto1Lerdo.": "GOMEZ PALACIO Y LERDO",
        "Mixto2Lerdo.": "GOMEZ PALACIO Y LERDO",
        "canatlan.": "CANATLAN DURANGO",
        "nombrededios.": "NOMBRE DE DIOS DURANGO",
        "nazas.": "NAZAS DURANGO",
        "cuencame.": "CUENCAME DURANGO",
        "sanjuandelrio.": "SAN JUAN DEL RIO DURANGO",
        "victoria.": "GUADALUPE VICTORIA DURANGO",
        "santiago.": "SANTIAGO PAPASQUIARO DURANGO",
        "elsalto.": "EL SALTO PUEBLO NUEVO DURANGO",
        "santamariadeloro.": "SANTA MARIA DEL ORO DURANGO",
    }

    materia = match_dict[doc_type]
    entidad = match_entidad_dict[doc_type]

    dict_to_return = {
        "materia": materia,
        "entidad": entidad,
    }
    return dict_to_return


def parse_field_b(b_field):
    """
       dict_to_return = {
            "fecha": yyyy/mm/dd",
            "fecha_insercion": datetime.now(),
            "fecha_tecnica": datetime(year=int(yyyy), month=int(mm), day=int(dd))
       }

    :param b_field:
    :return:
    """
    months = {
        "enero": "01",             # "January",
        "febrero": "02",           # "February",
        "marzo": "03",             # "March",
        "abril": "04",             # "April",
        "mayo": "05",              # "May",
        "junio": "06",             # "June",
        "julio": "07",             # "July",
        "agosto": "08",            # "August",
        "septiembre": "09",        # "September",
        "octubre": "10",          # "October",
        "noviembre": "11",        # "November",
        "diciembre": "12",        # "December",
    }

    # Finding dd
    dd_indexes = gm.find_number_indexes(b_field)
    dd = b_field[dd_indexes[0]:dd_indexes[1]]

    # Finding yyyy
    yyyy_indexes = gm.find_number_indexes("".join([x for x in reversed(b_field)]))
    if yyyy_indexes[0] != 0:
        yyyy = b_field[-yyyy_indexes[1]:-yyyy_indexes[0]]
    else:
        yyyy = b_field[-yyyy_indexes[1]:]

    # Finding mm
    mm = None
    for sp_mm in months.keys():
        if sp_mm in b_field.lower():
            mm = months[sp_mm]
            break

    if (mm is None) or (dd is None) or (yyyy is None):
        raise Exception("[ERROR] parse_field_b > (mm is None) or (dd is None) or (yyyy is None)")

    dict_to_return = {
        "fecha": f"{yyyy}/{mm}/{dd}",
        "fecha_insercion": datetime.now(),
        "fecha_tecnica": datetime(year=int(yyyy), month=int(mm), day=int(dd))
    }

    return dict_to_return, sp_mm


def clean_c_field(field_c_string: str):
    char_set = {
        "W": "II",
        "L": "I",
        "Y": "V",
        "1": "I",
        "!": "I",
    }
    tail = field_c_string.split("-")

    if len(tail) > 1:
        main_part_of_string = tail[0]
        tail = "-".join([x for x in tail[1:] if x not in ["", None]])
        out_tail_str = ''
        for char in tail:
            if char in [*char_set.keys()]:
                char = char_set[char]
            out_tail_str += char

        field_c_string = f"{main_part_of_string}-{out_tail_str}"
    return field_c_string


def parse_field_c(field_c_string):
    """
        Data example: 01215/2010
                      1276/2019-IV
                      222/2020-III
    :param field_c_string:
    :return:
    """
    field_c_items = field_c_string.split()
    field_c_items = [clean_c_field(x) for x in field_c_items]

    c_list = [x.strip().split("/") for x in field_c_items]
    for index in range(len(c_list)):
        if len(c_list[index]) == 1:
            c_list[index] = [c_list[index][0][:-4], c_list[index][0][-4:]]
    c_df = pd.DataFrame(
        c_list,
        columns=["article", "year"]
    )
    c_df = c_df.sort_values(by="year", ignore_index=True)

    # First row without "CC" puts in  i_field
    i_field = ""
    for row in c_df.itertuples():
        if "CC" in c_df.loc[0][0]:
            continue
        i_field += f"{row[1]}/{row[2]}"
        break

    # Other rows puts in c_field
    c_field = ""
    for row in c_df.itertuples():
        current_str = f"{row[1]}/{row[2]}"
        if current_str not in i_field:
            c_field += current_str + " "

    if c_field == "":
        c_field = i_field
        i_field = ""

    dict_to_return = {
        "expediente": c_field.strip(),
        "expediente_origen": i_field,
    }
    return dict_to_return


def parse_field_e(e_field_string):
    """
        Data example: INSTITUTO DEL FONDO NACIONAL DE LA VIVIENDA
                      PARA LOS TRABAJADORES (INFONAVIT) Vs YADIRA
                      ANGELES LANDA

    :param e_field_string:
    :return:
    """
    """
    # 1 - G = "(*)" or "(*(*))" and remove from string
    # 2 - locate of "Vs"
    #     2.1 if there is not "Vs" than E = remaining string
    # 3 - E = string before "Vs"
    # 4 - F = string after "Vs"
    patterns = [
        "(*)",      # G // also (*(*))
        "<-- Vs",   # E
        "Vs -->",   # F
    ]
    """
    e_field_string += " "

    # Getting brackets indexes
    open_bracket_indexes = gm.find_all_chars(e_field_string, "(")
    close_bracket_indexes = gm.find_all_chars(e_field_string, ")")
    brackets_indexes = np.append([[0, x] for x in open_bracket_indexes], [[1, x] for x in close_bracket_indexes], axis=0)
    if len(brackets_indexes) > 0:
        ind = np.argsort(brackets_indexes[:, 1])
        brackets_indexes = brackets_indexes[ind]

        # Find last brackets indexes
        open_index = None
        if brackets_indexes[-1][0] == 1:
            close_index = brackets_indexes[-1][1]
        else:
            close_index = None
        enc_counter = 0
        for bracket in reversed(brackets_indexes):
            if bracket[0] == 0:
                enc_counter -= 1
            else:
                enc_counter += 1

            # Break the loop if enc_counter is less than 1
            if enc_counter < 1:
                open_index = bracket[1]
                break

        if open_index is not None:
            if close_index is not None:
                if gm.find_string_indexes(e_field_string[close_index:].upper(), "Vs ".upper()) is None:
                    g_field = e_field_string[open_index:close_index + 1]
                    e_field_string = e_field_string[:open_index] + e_field_string[close_index + 1:]
                else:
                    g_field = ""
            else:
                g_field = e_field_string[open_index:]
                e_field_string = e_field_string[:open_index]
        else:
            g_field = ""
    else:
        g_field = ""

    # E = "<-- Vs"  //  F = "Vs -->"
    vs_location = gm.find_string_indexes(e_field_string.upper(), "Vs ".upper())
    if vs_location is not None:
        e_field = e_field_string[:vs_location[0]]
        f_field = e_field_string[vs_location[0] + 3:]
    else:
        e_field = e_field_string
        f_field = ""

    dict_to_return = {
        "actor": e_field,
        "demandado": f_field,
        "acuerdos": g_field,
    }
    return dict_to_return


def parse_field_d(d_field_string):
    after_strings = [
        "DISTRITO JUDICIAL",
    ]

    after_strings_locations_list = []
    for after_string in after_strings:
        after_strings_locations = gm.find_string_indexes(d_field_string, after_string)
        if after_strings_locations is not None:
            after_strings_locations_list.append(after_strings_locations)

    if len(after_strings_locations_list) > 0:
        after_strings_locations = after_strings_locations_list[0]
        j_field = d_field_string[:after_strings_locations[1]]
        d_field = d_field_string[after_strings_locations[1]:]
    else:
        j_field = ""
        d_field = d_field_string

    dict_to_return = {
        "tipo": d_field,
        "Organo_jurisdiccional_origen": j_field,
    }
    return dict_to_return


def parse_header(page_data_df):
    """

    :param page_data_df:
    :return: rec_header, sp_mm, no_row, page_size_row
    """
    rec_header = {}

    # Getting "No." row for bottom coordinate
    no_row = page_data_df.loc[page_data_df["text"] == "No.".upper()].reset_index(drop=True).iloc[0]

    # Getting page_size_row for top, left and right coordinates
    page_size_row = page_data_df.iloc[0]

    # Getting text inside header_ltrbbox
    header_ltrbbox = [page_size_row["right"] * 0.2, page_size_row["top"], page_size_row["right"], no_row["bottom"]]

    header_text_list = pp.get_text_inside_ltrbbox(header_ltrbbox, page_data_df)

    # Separate text by "Dictados el dia"
    dictados_index = [x for x in range(len(header_text_list)) if "dictados".upper() in header_text_list[x]][0]
    after_dictados_text = " ".join(header_text_list[dictados_index:])
    before_dictados_text = " ".join(header_text_list[:dictados_index])

    # A // JUZGADO
    start_pos = gm.find_string_indexes(before_dictados_text, "SUPERIOR DE JUSTICIA".upper())
    if start_pos is not None:
        start_pos = start_pos[1]
    else:
        raise IndexError("[ERROR] aux() > start_pos is None")
    end_pos = gm.find_string_indexes(before_dictados_text, "LISTA DE ACUERDOS".upper())
    if end_pos is not None:
        end_pos = end_pos[0]
    else:
        raise IndexError("[ERROR] aux() > end_pos is not None")
    rec_header["juzgado"] = before_dictados_text[start_pos:end_pos]

    # B // FECHA
    b_field = after_dictados_text[gm.find_number_indexes(after_dictados_text)[0]:]
    parsed_field_b, sp_mm = parse_field_b(b_field)
    rec_header.update(parsed_field_b)

    return rec_header, sp_mm, no_row, page_size_row


def aux(page_data_df):
    """
        return {
            "A": str,                      \n
            "B": str,                      \n
            "C": str,                      \n
            "D": str,                      \n
            "E": str,                      \n
        }

    :param page_data_df:
    :return:
    """

    # Parsing header
    rec_header, sp_mm, no_row, page_size_row = parse_header(page_data_df)

    # Getting top coordinate of "CORRESPONDIENTES" as bottom coordinate of the table
    mask = ["CORRESPONDIENTES".upper() in x for x in page_data_df["text"].values]
    corresp = page_data_df[mask].reset_index(drop=True)
    if len(corresp) > 0:
        bottom = corresp.iloc[0]["top"]
    else:
        # Finding sp_mm (Spanish month) to determine bottom coordinate of the table
        sp_mms = page_data_df.loc[page_data_df["text"] == sp_mm.upper()].reset_index(drop=True)

        if len(sp_mms) > 1:
            # Getting top coordinate of "DURANGO A ** DE sp_mm DE ****" as bottom coordinate of the table
            bottom = sp_mms.iloc[1]["top"]

        else:
            # Getting top coordinate of "PAGINA" as bottom coordinate of the table
            mask = ["PAGINA".upper() in x for x in page_data_df["text"].values]
            sp_mms = page_data_df[mask].reset_index(drop=True)
            bottom = sp_mms.iloc[0]["top"]

    # Getting data_df for table
    table_ltrbbox = [page_size_row["left"], no_row["top"], page_size_row["right"], bottom]
    table_df = pp.get_data_df_inside_ltrbbox(table_ltrbbox, page_data_df, margin=[0.005, 0.005])
    words_number = len(table_df)

    # Get table
    table_df = pp.table_from_data_df(table_df, table_check_strs=["/20", "S/N"])
    result = table_df.iloc[1:].to_json(orient="values")
    table_json = json.loads(result)

    # print(table_df)

    # Checking if the table columns number is 4
    if len(table_json) > 0:
        if len(table_json[0]) != 4:
            raise Exception("Wrong recognition: columns number is not equal 4")

    # Checking if the table words number is much less than the source data
    table_words_number = get_table_words_number(table_df)
    if table_words_number <= 0.5 * words_number:
        raise Exception(f"Not all data was recognised: recognised words number: {table_words_number}; "
                        f"source data words number: {words_number}")

    # Write data in records
    list_of_records = []
    for row_list in table_json:
        rec = {
            "C": row_list[1],
            "D": row_list[2],
            "E": row_list[3],
        }
        rec.update(rec_header)
        list_of_records.append(rec)

    return list_of_records


def parsing_pdf(pdf_path):

    record = {
        "actor": "",                                        # "E"
        "demandado": "",                                    # "F"
        "entidad": "",                                      # "+"
        "expediente": "",                                   # "C"
        "fecha": "",                                        # "B"
        "fuero": "COMUN",                                   # "d"
        "juzgado": "",                                      # "A"
        "tipo": "",                                         # "D"
        "acuerdos": "",                                     # "G"
        "monto": "",                                        # " "
        "fecha_presentacion": "",                           # " "
        "actos_reclamados": "",                             # " "
        "actos_reclamados_especificos": "",                 # " "
        "Naturaleza_procedimiento": "",                     # " "
        "Prestacion_demandada": "",                         # " "
        "Organo_jurisdiccional_origen": "",                 # "J"
        "expediente_origen": "",                            # "I"
        "materia": "",                                      # "H"
        "submateria": "",                                   # " "
        "fecha_sentencia": "",                              # " "
        "sentido_sentencia": "",                            # " "
        "resoluciones": "",                                 # " "
        "origen": "PODER JUDICIAL DEL ESTADO DE DURANGO",   # "d"
        "fecha_insercion": "",                              # "+"
        "fecha_tecnica": "",                                # "+"
    }

    # Doc type // part of filename
    file_name = gm.url_to_name(pdf_path)
    doc_type = file_name[gm.find_char_index(file_name, "_") + 1:gm.find_char_index(file_name, ".") + 1]

    # Parsing of all pages
    pdf_recs_list = []
    exit_key = False
    page_count = 0
    custom_dpi = 620
    mode_psm_3 = False
    threshold_mode = True
    # mode_psm_3 = True
    # threshold_mode = False

    while not exit_key:
        try:
            doc = convert_from_path(pdf_path, dpi=custom_dpi, thread_count=2)
            for page_number, page_data in enumerate(doc):
                if page_number < page_count:
                    continue
                # if page_number + 1 != 6:
                #     continue

                # Threshold recognition mode
                if threshold_mode:
                    dan.files.update({"threshold": f"{dan.dirs['images']}threshold.png"})
                    file_path = dan.files["threshold"]
                    page_data.save(file_path)
                    img = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
                    ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
                    cv.imwrite(file_path, thresh1)
                    page_data = np.array(thresh1)

                # Choosing the psm mode
                if mode_psm_3:
                    tesseract_config = "-l spa --psm 3"
                else:
                    tesseract_config = "-l spa --psm 4"

                # Getting page data as DataFrame
                page_data_df = pp.get_page_data_df(page_data, tesseract_config=tesseract_config)

                # Getting table data as fields A B C D E
                rec_list = aux(page_data_df)

                # Parsing of table data
                h = get_materia(doc_type)
                for rec_index in range(len(rec_list)):

                    # H // MATERIA and "entidad"
                    rec_list[rec_index].update(h)

                    # C I // EXPEDIENTE and EXPEDIENTE ORIGEN
                    parsed_c = parse_field_c(rec_list[rec_index]["C"])
                    rec_list[rec_index].update(parsed_c)
                    del rec_list[rec_index]["C"]

                    # E F G // ACTOR, DEMANDADO and ACUERDOS
                    parsed_e = parse_field_e(rec_list[rec_index]["E"])
                    rec_list[rec_index].update(parsed_e)
                    del rec_list[rec_index]["E"]

                    # D I // TIPO and ORGANO JURISDICCIONAL ORIGEN
                    parsed_d = parse_field_d(rec_list[rec_index]["D"])
                    rec_list[rec_index].update(parsed_d)
                    del rec_list[rec_index]["D"]

                # Removing double spaces and set UPPER case
                for rec in rec_list:
                    if rec["expediente"] == "":
                        raise ValueError('[ERROR] rec["expediente"] == ""')
                    if rec["tipo"] == "":
                        raise ValueError('[ERROR] rec["tipo"] == ""')

                    rec_to_append = {}
                    for key in record.keys():
                        if rec.get(key) is not None:
                            if type(rec[key]) == str:
                                clean_str = replace_wrong_recognitions(rec[key].upper().strip())
                                clean_str = dela_to_de_la(clean_str)
                                clean_str = remove_spec_chars(clean_str)
                                clean_str = gm.remove_repeated_char(clean_str)
                                # clean_str = clean_str.encode("utf-8")
                                rec_to_append.update({key: clean_str})
                            else:
                                rec_to_append.update({key: rec[key]})
                        else:
                            rec_to_append.update({key: record[key]})
                    pdf_recs_list.append(rec_to_append)

                page_count += 1
                custom_dpi = 620
                mode_psm_3 = False
                threshold_mode = True
            break
        except Exception as _ex:
            # Increase image dpi
            custom_dpi += 20
            print(f"[WARNING] {_ex} | custom_dpi += 20 = {custom_dpi} | Next attempt")

            if custom_dpi >= 700 and not mode_psm_3:
                print("mode --psm 3 enabled | custom_dpi = 620 | Next attempt")
                custom_dpi = 620
                mode_psm_3 = True

            if custom_dpi >= 700 and mode_psm_3:
                print("threshold mode disabled | custom_dpi = 120 | Next attempt")
                custom_dpi = 120
                threshold_mode = False

            # Exit if threshold mode recognition failed too
            if custom_dpi >= 240 and not threshold_mode:
                print(f"{Tags.LightYellow}[ERROR] Recognition failed{Tags.ResetAll}")
                args["failed_processing"] += 1
                print("Number of unprocessed files: ", args["failed_processing"])
                exit_key = True

    # Save to json file
    # if not exit_key:
    #     json_file_path = pdf_path[:-3] + "json"
    #     print("Saving to:", json_file_path, end=" .... ")
    #     with open(json_file_path, "w") as json_file:
    #         json_file.write(json.dumps(pdf_recs_list, indent=4, cls=DateTimeEncoder, ensure_ascii=False).encode('utf8').decode())
    #     print(f"{Tags.LightYellow}Saved{Tags.ResetAll}")
    # else:
    #     print(f"{Tags.LightYellow}[ERROR] Saving error{Tags.ResetAll}")
    #     args["failed_processing"] += 1
    #     print("Number of unprocessed files: ", args["failed_processing"])

    return pdf_recs_list


# # ===== Start app =================================================================================== Start app =====
...
# # ===== Start app =================================================================================== Start app =====


def scrape_date(files_date):

    dan.create_dirs()

    # Getting values for url_generator
    for _ in range(3):
        try:
            values_for_url = scrape_values_for_urls()

            # Creating urls of files
            files_urls = get_files_urls(
                files_date=files_date,
                values_for_url=values_for_url
            )

            # Save file to temporary folder
            for _ in range(3):
                try:
                    asyncio.run(save_reports(files_urls, files_date))
                    break
                except asyncio.TimeoutError:
                    continue

            # Getting list of pdf_path
            all_pdf_paths = get_all_files_by_extension(dan.dirs["temp_dir"], "pdf")

            # Parsing pdf files
            records_list = []
            for pdf_path in all_pdf_paths:
                print("\nProcessing:", pdf_path)
                records_list = parsing_pdf(pdf_path)

                # Add records to db
                if len(records_list) > 0:
                    add_records_to_db(records_list)
                else:
                    print("[WARNING] No data to save")

            # pdf_path = "/home/user_name/PycharmProjects/008_TECH_SPEC/app/temp/capital/17-3-2020_seccu.pdf"
            # pdf_path = "/home/user_name/PycharmProjects/008_TECH_SPEC/app/temp/capital/17-3-2020_civ4.pdf"
            # records_list = parsing_pdf(pdf_path)

            # Delete all duplicates from db
            delete_all_duplicates()

            # Delete temp folder
            dan.remove_dirs()
            break

        except ServerIsDown:
            sleep(2 * 60 * 60)


def check_and_scrape_dates(dates_list):
    for date_item in dates_list:
        if check_date(date_item):
            scrape_date(date_item)


def start_app():

    print(args["stdout"])
    print(dan, end="\n\n")
    dan.remove_dirs()

    # Getting all dates between star_date and end_date
    dates_list = gm.dates_between(args["start_date"], args["end_date"])

    try:
        # Scrape all the specified dates
        check_and_scrape_dates(dates_list)

        if args["last_today"]:
            while True:
                print(f"\n{Tags.LightYellow}Sleep 2 days from: {datetime.today()}{Tags.ResetAll}")
                sleep(2 * 24 * 60 * 60)

                # Getting all dates between start_date and today, check in db and scrape
                last_dates_list = gm.dates_between(args["start_date"])
                check_and_scrape_dates(last_dates_list)

    except KeyboardInterrupt:
        print("EXIT ... ")
        dan.remove_dirs()
    finally:
        print("Number of unprocessed files: ", args["failed_processing"])
        sys.exit()


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    start_app()

