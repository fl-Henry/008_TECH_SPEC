import os
import sys
import json
import random
import pymongo
import asyncio
import aiohttp
import aiofiles
import argparse
import requests
import pandas as pd

# from aiohttp_socks import ChainProxyConnector, ProxyConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from pdfquery import PDFQuery
from time import sleep

# Custom imports
import pdf_parser as pp
import general_methods as gm

from general_methods import DaNHandler, arg_parser, dates_between, url_to_name, replace_chars, find_char_index, \
    find_number_index

from print_tags import Tags


# # ===== General Variables =================================================================== General Variables =====
...
# # ===== General Variables =================================================================== General Variables =====

...
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
    materia = match_dict[doc_type]
    return materia


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


# # ===== Parsing Methods ======================================================================= Parsing Methods =====
...
# # ===== Parsing Methods ======================================================================= Parsing Methods =====


def aux(page_tag):
    """
        return {
            "actor": "",                          \n
            "demandado": "",                      \n
            "entidad": "",                        \n
            "expediente": "",                     \n
            "fecha": "",                          \n
            "fuero": "",                          \n
            "juzgado": "",                        \n
            "tipo": "",                           \n
            "acuerdos": "",                       \n
            "monto": "",                          \n
            "fecha_presentacion": "",             \n
            "actos_reclamados": "",               \n
            "actos_reclamados_especificos": "",   \n
            "Naturaleza_procedimiento": "",       \n
            "Prestación_demandada": "",           \n
            "Organo_jurisdiccional_origen": "",   \n
            "expediente_origen": "",              \n
            "materia": "",                        \n
            "submateria": "",                     \n
            "fecha_sentencia": "",                \n
            "sentido_sentencia": "",              \n
            "resoluciones": "",                   \n
            "origen": "",                         \n
            "fecha_insercion": "",                \n
            "fecha_tecnica": "",                  \n
        }

    :param page_tag:
    :return:
    """

    rec_header = {}

    # Bboxes that edge/border the header
    tblr_bbox = {
        "top": (236.04, 915.72, 503.381, 927.72),
        "bottom": (240.96, 849.72, 498.436, 861.72),
        "left": (178.68, 887.4, 560.777, 899.4),
        "right": (178.68, 887.4, 560.777, 899.4),
    }
    bbox_to_find = pp.tblr_to_bbox(tblr_bbox, margin=0.02)

    # Get text of header
    header_text_list = pp.text_inside_bbox(page_tag, bbox_to_find)

    # A // JUZGADO
    start_pos = gm.find_string_indexes(header_text_list[0], "SUPERIOR DE JUSTICIA")[1]
    end_pos = gm.find_string_indexes(header_text_list[0], "LISTA DE ACUERDOS")[0]
    rec_header["A"] = header_text_list[0][start_pos:end_pos]

    # B // FECHA TODO: format date yyyy/mm/dd
    rec_header["B"] = header_text_list[1][find_number_index(header_text_list[1]):-1]

    # Parsing of table ================================================================================================
    ...
    # Finding DURANGO,
    durango_position = pp.find_position("DURANGO,", page_tag)

    if durango_position is None:
        # Getting PAGINA bbox
        pagina_position = pp.find_position("PAGINA", page_tag)
        pagina_tag = pp.get_tag_by_attr_position(pagina_position, page_tag)
        pagina_bbox = pp.get_bbox(0, pagina_tag)
        bottom_bbox = pagina_bbox
    else:
        # Getting DURANGO, bbox
        durango_position = pp.find_position("DURANGO,", page_tag)
        durango_tag = pp.get_tag_by_attr_position(durango_position, page_tag)
        durango_bbox = pp.get_bbox(0, durango_tag)
        bottom_bbox = durango_bbox
    bottom_bbox[1] = bottom_bbox[3]

    # Getting page_bbox
    page_bbox = pp.get_bbox(0, page_tag)

    # Getting No. bbox
    no_position = pp.find_position("No.", page_tag)
    no_tag = pp.get_tag_by_attr_position(no_position, page_tag)
    no_bbox = pp.get_bbox(0, no_tag)

    # Bboxes that edge/border the table
    tblr_bbox = {
        "top": no_bbox,
        "bottom": bottom_bbox,
        "left": no_bbox,
        "right": page_bbox,
    }
    bbox_to_find = pp.tblr_to_bbox(tblr_bbox, margin=0.005)

    # Get table
    table_df = pp.get_table(page_tag, bbox_to_find, margin_x=0.1, margin_y=0.13)
    result = table_df.to_json(orient="values")
    table_json = json.loads(result)

    print(table_df)
    # print(table_json)

    # Write data in records
    list_of_records = []
    for row_list in table_json:
        rec = {
            "A": rec_header["A"],
            "B": rec_header["B"],
            "C": row_list[1],
            "D": row_list[2],
            "E": row_list[3],
        }
        list_of_records.append(rec)

    return list_of_records


def parse_field_c(field_c_string):
    c_list =[x.strip() for x in field_c_string.split()]

    if len(c_list) > 1:
        i_field = ""
        c_field_list = []
        for item in c_list:
            if len(c_field_list) == 0:
                c_field_list.append(item)
            elif "CC" in item:
                if len(c_field_list) > 1:
                    i_field = c_field_list[-1]
                    c_field_list[-1] = item
                else:
                    c_field_list.append(item)
            elif ("CC" not in c_field_list[-1]) and (int(item[-4:]) < int(c_field_list[-1][-4:])):
                if len(i_field) == 0:
                    i_field = item
                else:
                    if int(item[-4:]) < int(i_field[-4:]):
                        c_field_list.append(i_field)
                        i_field = item
                    else:
                        bl = c_field_list[-1]
                        c_field_list[-1] = item
                        c_field_list.append(bl)
            elif int(item[-4:]) > int(c_field_list[-1][-4:]):
                bl = c_field_list[-1]
                c_field_list[-1] = item
                c_field_list.append(bl)
            else:
                c_field_list.append(item)

            print(c_field_list)
            print(i_field)
            print()

        c_i_dict = {
            "C": " ".join(c_field_list),
            "I": i_field,
        }
    else:
        c_i_dict = {
            "C": c_list[0],
            "I": "",
        }

    return c_i_dict


def parsing_pdf(pdf_path):

    record = {
        "actor": "",                         # "actor"
        "demandado": "",                     # "defendant"
        "entidad": "",                       # "entity"
        "expediente": "",                    # "file"
        "fecha": "",                         # "date"
        "fuero": "",                         # "jurisdiction"
        "juzgado": "",                       # "court"
        "tipo": "",                          # "type"
        "acuerdos": "",                      # "agreements"
        "monto": "",                         # "amount"
        "fecha_presentacion": "",            # "date filed"
        "actos_reclamados": "",              # "claimed acts"
        "actos_reclamados_especificos": "",  # "specific claimed acts"
        "Naturaleza_procedimiento": "",      # "Nature of the proceeding"
        "Prestación_demandada": "",          # "Benefit demanded"
        "Organo_jurisdiccional_origen": "",  # "Jurisdiction of origin"
        "expediente_origen": "",             # "original case file"
        "materia": "",                       # "subject matter"
        "submateria": "",                    # "sub-subject matter"
        "fecha_sentencia": "",               # "date of judgment"
        "sentido_sentencia": "",             # "sense judgment"
        "resoluciones": "",                  # "resolutions"
        "origen": "",                        # "origin"
        "fecha_insercion": "",               # "date of insertion"
        "fecha_tecnica": "",                 # "technical date"
    }

    # Convert PDF to XML
    # xml_path = pp.convert_pdf_to_xml(pdf_path)
    xml_path = "./temp/capital/2792017_aux1.xml"

    # Parsing whole xml document
    parsed_xml = pp.parse_xml(xml_path)

    parsed_xml.update({"xml_text": replace_chars(parsed_xml["xml_text"])})

    # Getting the whole page
    pages_tags = pp.get_all_tags_by_name("LTPage", parsed_xml["xml_text"])

    # Doc type // part of filename
    file_name = url_to_name(xml_path)
    doc_type = file_name[find_char_index(file_name, "_") + 1:find_char_index(file_name, ".") + 1]

    # Parsing of all pages
    for page_tag in pages_tags:
        print("\n======================================== Page ========================================\n")
        # Choosing relevant parsing script
        if doc_type in ["aux1.", "aux2."]:

            # Getting table data as fields A B C D E
            rec_list = aux(page_tag)

            # Parsing of table data
            h = get_materia(doc_type)
            for rec_index in range(len(rec_list)):

                # H // MATERIA
                rec_list[rec_index].update({"H": h})

                # C I // EXPEDIENTE and EXPEDIENTE ORIGEN
                parsed_c = parse_field_c(rec_list[rec_index]["C"])
                rec_list[rec_index].update(parsed_c)

                parsed_e = parse_field_e(rec_list[rec_index]["E"])

                sys.exit()
            # print(rec_list)
            # print("\n")

    sys.exit()
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

    # Getting values for url_generator
    # values_for_url = scrape_values_for_urls()

    # # Creating urls of files
    # files_urls = get_files_urls(
    #     star_date=args['start_date'],
    #     end_date=args['end_date'],
    #     values_for_url=values_for_url
    # )

    # # Save file to temporary folder
    # asyncio.run(save_reports(files_urls))

    # Connect to DB
    # db_client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Parsing pdf files
    pdf_path = "./temp/capital/2792017_aux1.pdf"
    dicts = parsing_pdf(pdf_path)

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

