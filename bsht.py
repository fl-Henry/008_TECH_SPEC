import os
import sys
import shutil
import random
import pymongo
import argparse
import pdfquery
import requests
import numpy as np
import pandas as pd

from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from time import sleep


from general_methods import replace_chars, url_to_name, url_parent


def find_tag_name(char_index, dom):
    for tag_name_close_index in range(len(dom[char_index:])):
        if dom[char_index + tag_name_close_index] == " ":
            return dom[char_index + 1:char_index + tag_name_close_index]


def get_tag_by_attr_position(char_index, dom):

    # Finding open bracket for tag
    open_index = 0
    for open_bracket_index in range(char_index):
        if dom[char_index - open_bracket_index] == "<":
            open_index = char_index - open_bracket_index
            break

    # Getting tag name
    tag_name = find_tag_name(open_index, dom)

    # Finding close bracket for tag
    close_index = 0
    for close_bracket_index in range(len(dom[char_index:])):
        current_position = char_index + close_bracket_index
        if dom[current_position:current_position + len(tag_name) + 3] == f"</{tag_name}>":
            close_index = current_position + len(tag_name) + 3
            break

    return dom[open_index:close_index]


def get_bbox(char_index, dom):
    # Finding open bracket for bbox
    open_index = char_index
    if dom[char_index + 7] == "[":
        open_index = char_index + 7
    else:
        for open_bracket_index in range(len(dom[char_index:])):
            if dom[char_index + open_bracket_index] == "[":
                open_index = char_index + open_bracket_index + 1
                break

    # Finding close bracket for tag
    close_index = 0
    for close_bracket_index in range(len(dom[char_index:])):
        if dom[char_index + close_bracket_index] == "]":
            close_index = char_index + close_bracket_index
            break

    bbox = [float(x.strip()) for x in dom[open_index:close_index].split(",")]

    return bbox


def relative_bbox_to_bbox(relative_bbox, page_bbox):
    """

    :param relative_bbox: tuple[float]  | (20, 20, 80, 80) -> (20%, 20%, 80%, 80%)
    :param page_bbox: tuple[float]      | (0, 0, 300, 600) -> (x0, y0, x1, y1)
    :return:
    """
    relative_bbox = np.array(relative_bbox)
    page_bbox = np.array((page_bbox[2], page_bbox[3], page_bbox[2], page_bbox[3])).transpose()
    return np.multiply(relative_bbox * 0.01, page_bbox)


def check_nesting(bbox, parent_bbox):
    """

    :param bbox: tuple[float]             | (200, 200, 300, 600) -> (x0, y0, x1, y1)
    :param parent_bbox: tuple[float]      | (200, 200, 300, 600) -> (x0, y0, x1, y1)
    :return:
    """
    # Checking types of input
    if (type(bbox) == list) or (type(bbox) == tuple):
        bbox = np.array(bbox)
    elif type(bbox) == np.ndarray:
        pass
    else:
        print("[ERROR] check_nesting > wrong bbox type:", type(bbox), "bbox:", bbox)

    if (type(parent_bbox) == list) or (type(parent_bbox) == tuple):
        parent_bbox = np.array(parent_bbox)
    elif type(parent_bbox) == np.ndarray:
        pass
    else:
        print("[ERROR] check_nesting > wrong parent_bbox type:", type(parent_bbox), "parent_bbox:", parent_bbox)

    check_bbox = parent_bbox - bbox
    filter_bbox = check_bbox < 0
    if len(check_bbox[filter_bbox]) > 0:
        return False
    else:
        return True


def get_tag_text(tag):
    """

    :param tag: str
    :return:
    """
    text = ""
    key_to_write = False
    for char in tag:
        if char == "<":
            key_to_write = False
        if key_to_write:
            text += char
        if char == ">":
            key_to_write = True
    return text


def find_inside_bbox(parsed_xml, bbox_to_find):
    """

    :param parsed_xml: dict[str, tuple[float]   | {"xml_text": <xml_text>, "page_bbox": (0, 0, 100, 100)}
    :param bbox_to_find: tuple[float]           | (0, 0, 10, 10)
    :return:
    """

    # Check all bboxes if they are in the bbox_to_find
    for char_index in range(len(parsed_xml["xml_text"]) - 3):
        if parsed_xml["xml_text"][char_index:char_index + 4] == "bbox":
            bbox = get_bbox(char_index, parsed_xml["xml_text"])
            if check_nesting(bbox, bbox_to_find):
                tag = get_tag_by_attr_position(char_index, parsed_xml["xml_text"])
                print(tag)
                tag_text = get_tag_text(tag)
                print(tag_text)


def parse_xml(xml_path):
    with open(xml_path, "r") as xml_file:
        xml_text = xml_file.read()

    # Finding page bbox
    page_bbox = None
    for char_index in range(len(xml_text) - 3):
        if xml_text[char_index:char_index + 4] == "bbox":
            bbox = get_bbox(char_index, xml_text)
            if (bbox[0] == 0) and (bbox[1] == 0):
                page_bbox = bbox
                break
            else:
                continue

    if page_bbox is None:
        print("[ERROR] xml_find > page_bbox is None")
        print("xml_text:", xml_text)
        raise ValueError

    return {"xml_text": xml_text, "page_bbox": page_bbox}

    # # Find all bboxes
    # for char_index in range(len(xml_text) - 3):
    #     if xml_text[char_index:char_index + 4] == "bbox":
    #         bbox_list = get_bbox(char_index, xml_text)
    #         print(bbox_list)
    #         # tag = get_tag_by_attr_position(char_index, xml_text)
    #         # print(tag)


def parsing_pdf(file_path):
    """"""
    """
    {
        "actor": ,                        # "actor"
        "demandado": ,                    # "defendant"
        "entidad": ,                      # "entity"
        "expediente": ,                   # "file"
        "fecha": ,                        # "date"
        "fuero": ,                        # "jurisdiction"
        "juzgado": ,                      # "court"
        "tipo": ,                         # "type"
        "acuerdos": ,                     # "agreements"
        "monto": ,                        # "amount"
        "fecha_presentacion": ,           # "date filed"
        "actos_reclamados": ,             # "claimed acts"
        "actos_reclamados_especificos": , # "specific claimed acts"
        "Naturaleza_procedimiento": ,     # "Nature of the proceeding"
        "Prestación_demandada": ,         # "Benefit demanded"
        "Organo_jurisdiccional_origen": , # "Jurisdiction of origin"
        "expediente_origen": ,            # "original case file"
        "materia": ,                      # "subject matter"
        "submateria": ,                   # "sub-subject matter"
        "fecha_sentencia": ,              # "date of judgment"
        "sentido_sentencia": ,            # "sense judgment"
        "resoluciones": ,                 # "resolutions"
        "origen": ,                       # "origin"
        "fecha_insercion": ,              # "date of insertion"
        "fecha_tecnica": ,                # "technical date"
    }
    """

    record = {
        "actor": str,
        "demandado": str,
        "entidad": str,
        "expediente": str,
        "fecha": str,
        "fuero": str,
        "juzgado": str,
        "tipo": str,
        "acuerdos": str,
        "monto": str,
        "fecha_presentacion": str,
        "actos_reclamados": str,
        "actos_reclamados_especificos": str,
        "Naturaleza_procedimiento": str,
        "Prestación_demandada": str,
        "Organo_jurisdiccional_origen": str,
        "expediente_origen": str,
        "materia": str,
        "submateria": str,
        "fecha_sentencia": str,
        "sentido_sentencia": str,
        "resoluciones": str,
        "origen": str,
        "fecha_insercion": str,
        "fecha_tecnica": str,
    }

    pdf = pdfquery.PDFQuery(file_path)
    pdf.load()

    pdf_name = url_to_name(file_path)
    xml_name = pdf_name[:-3] + "xml"
    file_dir = url_parent(file_path)
    xml_path = f"{file_dir}{xml_name}"

    # convert the pdf to XML
    pdf.tree.write(xml_path, pretty_print=False)

    # # Extract the text from the elements
    # text = [t.text for t in text_elements]
    # print(text)


def main():
    path = "./temp/capital/2642023_aux1.pdf"
    xml_path = "./temp/capital/2642023_aux1.xml"
    # parsing_pdf(path)

    bbox_to_find = (100, 100, 300, 300)
    parsed_xml = parse_xml(xml_path)

    relative_bbox = (20, 50, 90, 90)
    bbox_to_find = relative_bbox_to_bbox(relative_bbox, parsed_xml["page_bbox"])
    print(bbox_to_find)
    print(parsed_xml["page_bbox"])
    # [236.04, 915.72, 503.381, 927.72]
    # check_nesting(relative_bbox, bbox_to_find)
    # find_inside_bbox(parsed_xml, bbox_to_find)

if __name__ == '__main__':
    main()

