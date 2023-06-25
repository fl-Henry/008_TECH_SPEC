import json
import os
import sys
import shutil
import random
import codecs
import pymongo
import argparse
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from time import sleep

import pdf_parser as pp
import general_methods as gm

# def get_json_from_fin


db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = db_client["raw"]
collection = db["juzgados"]


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

    # getting brackets indexes
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
                g_field = e_field_string[open_index:close_index + 1]
                e_field_string = e_field_string[:open_index] + e_field_string[close_index + 1:]
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



def main():
    pass

    all_pdf_paths = [
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_canatlan.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_cuencame.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_nombrededios.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_santiago.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_santamariadeloro.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_victoria.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_sanjuandelrio.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/foraneos/1732020_elsalto.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_mer3.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_aux2.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_fam3.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_civ4.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_civ2.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_fam1.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_fam4.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_fam2.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_fam5.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_seccc.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_mer4.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_seccu.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_civ3.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_mer2.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_aux1.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/capital/1732020_mer1.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Fam1GP.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Mixto1Lerdo.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Mixto2Lerdo.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_AuxMixtoGP.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Fam3GP.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Civ2GP.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Fam2GP.pdf',
        '/home/user_name/PycharmProjects/008_TECH_SPEC/temp/lerdo/1732020_Civ1GP.pdf'
    ]

    str_lst = [
        " ORDINARIO CIVIL (FAMILIAR)  ",
        "DELGADO REYES VS",
        " ORDINARIO CIVIL (FAMILIAR",
        "TORRES LOPEZ A BIENES DE: NAHUL LUNA Y SENTENCIA)",
    ]
    # for str_ in str_lst:
    #     print(str_)
    #     print(parse_field_e(str_))

    path = "./test_char.json"
    json_data = [{"key": "\u00b0"}]
    with open(path, "w") as f:
        f.write(json.dumps(json_data, indent=4, ensure_ascii=False).encode('utf8').decode())

"""




"""

def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
