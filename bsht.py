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



def replace_wrong_recognitions(in_str):
    replace_dict = {
        "‘TER.": "1ER.",
        "TER.": "1ER.",
        "‘ER.": "1ER.",
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



def main():
    pass
    # sers = pd.Series([0, 1, 2])
    # print(sers)
    # sers[3] = 3
    # print(sers)
    # types_dict = {col: "int" for col in ["left", "top", "width", "height", "right", "bottom"]}
    #
    # print(types_dict)

    # str_s = [
    #     "TERCERO DE LO CIVIL ‘ER. DISTRITO JUDICIAL ORD...",
    #     "SEGUNDO DELO FAMILIAR TER. DISTRITO JUDICIAL C...",
    #     "TERCERO DE LO CIVIL ‘TER. DISTRITO JUDICIAL OR..."
    # ]
    #
    # for str_ in str_s:
    #     res = replace_wrong_recognitions(str_)
    #     print(str_)
    #     print(res)
    #     print()

    for x in range(0, 8):
        print(-x)

def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
