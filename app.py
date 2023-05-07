import os
import sys
import json
import random
import asyncio
import aiohttp
import aiofiles
import argparse
import requests
import numpy as np
import pandas as pd

# sudo apt-get install gnupg
# echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
# sudo apt-get update
# sudo apt-get install -y mongodb-org
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


# # ===== General Variables =================================================================== General Variables =====
...
# # ===== General Variables =================================================================== General Variables =====

...
# Parsing the arguments
args = gm.arg_parser()
dan = gm.DaNHandler()

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


def get_files_urls(star_date, end_date, values_for_url):
    # Getting all dates between star_date and end_date
    dates_list = gm.dates_between(star_date, end_date)

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
                    file_date = gm.url_to_name(file_url, iter_count=2)
                    file_name = gm.url_to_name(file_url)
                    file_path = f"{file_dir}{file_date}_{file_name}"
                    task = asyncio.create_task(write_file(session, file_url, file_path, stdout_key=True))
                    tasks.append(task)

        await asyncio.gather(*tasks)


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
        "aux1.": "DE LA CAPITAL",
        "aux2.": "DE LA CAPITAL",
        "civ2.": "DE LA CAPITAL",
        "civ3.": "DE LA CAPITAL",
        "civ4.": "DE LA CAPITAL",
        "fam1.": "DE LA CAPITAL",
        "fam2.": "DE LA CAPITAL",
        "fam3.": "DE LA CAPITAL",
        "fam4.": "DE LA CAPITAL",
        "fam5.": "DE LA CAPITAL",
        "mer1.": "DE LA CAPITAL",
        "mer2.": "DE LA CAPITAL",
        "mer3.": "DE LA CAPITAL",
        "mer4.": "DE LA CAPITAL",
        "merOral.": "DE LA CAPITAL",
        "seccc.": "DE LA CAPITAL",
        "seccu.": "DE LA CAPITAL",
        "cjmf1.": "DE LA CAPITAL",
        "cjmf2.": "DE LA CAPITAL",
        "tribl.": "DE LA CAPITAL",
        "Civ1GP.": "GOMEZ PALACIO Y LERDO",
        "Civ2GP.": "GOMEZ PALACIO Y LERDO",
        "Fam1GP.": "GOMEZ PALACIO Y LERDO",
        "Fam2GP.": "GOMEZ PALACIO Y LERDO",
        "AuxMixtoGP.": "GOMEZ PALACIO Y LERDO",
        "Fam3GP.": "GOMEZ PALACIO Y LERDO",
        "secccGP.": "GOMEZ PALACIO Y LERDO",
        "seccuGP.": "GOMEZ PALACIO Y LERDO",
        "triblG.": "GOMEZ PALACIO Y LERDO",
        "Mixto1Lerdo.": "GOMEZ PALACIO Y LERDO",
        "Mixto2Lerdo.": "GOMEZ PALACIO Y LERDO",
        "canatlan.": "CANATLAN",
        "nombrededios.": "NOMBRE DE DIOS",
        "nazas.": "NAZAS",
        "cuencame.": "CUENCAME",
        "sanjuandelrio.": "SAN JUAN DEL RIO",
        "elsalto.": "GUADALUPE VICTORIA",
        "santamariadeloro.": "SANTIAGO PAPASQUIARO",
        "victoria.": "EL SALTO PUEBLO NUEVO",
        "santiago.": "SANTA MARIA DEL ORO",
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
        "enero": "1",             # "January",
        "febrero": "2",           # "February",
        "marzo": "3",             # "March",
        "abril": "4",             # "April",
        "mayo": "5",              # "May",
        "junio": "6",             # "June",
        "julio": "7",             # "July",
        "agosto": "8",            # "August",
        "septiembre": "9",        # "September",
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


def parse_field_c(field_c_string):
    c_list = [x.strip().split("/") for x in field_c_string.split()]
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
    """"""
    """
    # TODO: 1 - G = "(*)" or "(*(*))" and remove from string
    #       2 - locate of "Vs"
    #           2.1 if there is not "Vs" than E = remaining string
    #       3 - E = string before "Vs"
    #       4 - F = string after "Vs"
    patterns = [
        "(*)",      # G // also (*(*))
        "<-- Vs",   # E
        "Vs -->",   # F
    ]
    """

    # G = "( -->"
    g_field_location = gm.find_string_indexes(e_field_string, "(")
    if g_field_location is not None:
        g_field = e_field_string[g_field_location[0]:]
        e_field_string = e_field_string[:g_field_location[0]]
    else:
        g_field = ""

    # E = "<-- Vs"  //  F = "Vs -->"
    vs_location = gm.find_string_indexes(e_field_string, "Vs")
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
    header_ltrbbox = [page_size_row["left"], page_size_row["top"], page_size_row["right"], no_row["bottom"]]
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
        raise IndexError("[ERROR] aux() > start_pos is not None")
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

    # Parsing of table
    ...
    # Finding sp_mm (Spanish month) to determine bottom coordinate of the table
    sp_mms = page_data_df.loc[page_data_df["text"] == sp_mm.upper()].reset_index(drop=True)

    if len(sp_mms) > 1:
        # Getting top coordinate of "DURANGO A ** DE sp_mm DE ****" as bottom coordinate of the table
        bottom = sp_mms.iloc[1]["top"]

    else:
        # Getting top coordinate of "PAGINA" as bottom coordinate of the table
        sp_mms = page_data_df.loc[page_data_df["text"] == "PAGINA".upper()].reset_index(drop=True)
        bottom = sp_mms.iloc[0]["top"]

    # Getting data_df for table
    table_ltrbbox = [page_size_row["left"], no_row["top"], page_size_row["right"], bottom]
    table_df = pp.get_data_df_inside_ltrbbox(table_ltrbbox, page_data_df, margin=[0.005, 0.005])

    # Get table
    table_df = pp.table_from_data_df(table_df)



    print(table_df)
    sys.exit()

    if len(table_df) == 0:
        return []



    result = table_df.to_json(orient="values")
    table_json = json.loads(result)

    # print(table_df)
    # print(table_json)
    ...
    # Write data in records
    list_of_records = []
    # TODO: If "No. Expediente"
    try:
        for row_list in table_json:
            rec = {
                "C": row_list[1],
                "D": row_list[2],
                "E": row_list[3],
            }
            rec.update(rec_header)
            list_of_records.append(rec)
    except IndexError as _ex:
        print(f"[ERROR] Write data in records > {_ex}")
        return []

    return list_of_records


def parsing_pdf(pdf_path):

    record = {
        "actor": "",                         # "E"
        "demandado": "",                     # "F"
        "entidad": "",                       # "+"
        "expediente": "",                    # "C"
        "fecha": "",                         # "B"
        "fuero": "",                         # "d"
        "juzgado": "",                       # "A"
        "tipo": "",                          # "D"
        "acuerdos": "",                      # "G"
        "monto": "",                         # " "
        "fecha_presentacion": "",            # " "
        "actos_reclamados": "",              # " "
        "actos_reclamados_especificos": "",  # " "
        "Naturaleza_procedimiento": "",      # " "
        "Prestación_demandada": "",          # " "
        "Organo_jurisdiccional_origen": "",  # "J"
        "expediente_origen": "",             # "I"
        "materia": "",                       # "H"
        "submateria": "",                    # " "
        "fecha_sentencia": "",               # " "
        "sentido_sentencia": "",             # " "
        "resoluciones": "",                  # " "
        "origen": "",                        # "d"
        "fecha_insercion": "",               # "+"
        "fecha_tecnica": "",                 # "+"
    }

    default_record = {
        "fuero": "COMUN",
        "origen": "PODER JUDICIAL DEL ESTADO DE DURANGO",
    }

    # Doc type // part of filename
    file_name = gm.url_to_name(pdf_path)
    doc_type = file_name[gm.find_char_index(file_name, "_") + 1:gm.find_char_index(file_name, ".") + 1]

    # Parsing of all pages
    pdf_recs_list = []
    doc = convert_from_path(pdf_path)
    for page_number, page_data in enumerate(doc):
        if page_number + 1 != 2:
            continue

        # print("\n==================================== Page ====================================\n")
        rec_list = []

        # Getting page data as DataFrame
        page_data_df = pp.get_page_data_df(page_data)

        # Choosing relevant parsing script
        # list_of_doc_types = ["aux1.", "aux2.", "civ2.", ""]
        # if doc_type in ["aux1.", "aux2."]:
        if True:
            # Getting table data as fields A B C D E
            rec_list = aux(page_data_df)

            print(page_data_df)
            sys.exit()


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

                # + default records
                rec_list[rec_index].update(default_record)

        # Removing double spaces and set UPPER case
        for rec in rec_list:
            for key in rec.keys():
                if type(rec[key]) == str:
                    rec.update({key: gm.remove_repeated_char(rec[key].upper().strip())})
            pdf_recs_list.append(rec)

    # Save to json file
    json_file_path = pdf_path[:-3] + "json"
    print("Saving to:", json_file_path, end=".... ")
    with open(json_file_path, "w") as json_file:
        json_file.write(json.dumps(pdf_recs_list, indent=4, cls=DateTimeEncoder))
    print(f"{Tags.LightYellow}Saved{Tags.ResetAll}")

    return None


# # ===== Start app =================================================================================== Start app =====
...
# # ===== Start app =================================================================================== Start app =====


def start_app():
    start_time = datetime.now()

    # print(args["stdout"])
    # print(dan)

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

    # # Getting values for url_generator
    # values_for_url = scrape_values_for_urls()
    #
    # # Creating urls of files
    # files_urls = get_files_urls(
    #     star_date=args['start_date'],
    #     end_date=args['end_date'],
    #     values_for_url=values_for_url
    # )
    #
    # # Save file to temporary folder
    # asyncio.run(save_reports(files_urls))

    # Connect to DB
    # db_client = pymongo.MongoClient("mongodb://localhost:27017/")

    # # Parsing pdf files
    # pdf_path = "./temp/capital/2792017_aux1.pdf"
    # pdf_path = "/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/2792017_Fam3GP.pdf"
    # dicts = parsing_pdf(pdf_path)

    all_pdf_paths = get_all_files_by_extension(dan.dirs["temp_dir"], "pdf")
    for pdf_path in all_pdf_paths:
        print("\nProcessing:", pdf_path)
        dicts = parsing_pdf(pdf_path)
        sys.exit()

    # Delete temp folder
    # dan.remove_dirs()
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

