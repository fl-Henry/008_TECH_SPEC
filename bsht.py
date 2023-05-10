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


def main():
    pass
    # sers = pd.Series([0, 1, 2])
    # print(sers)
    # sers[3] = 3
    # print(sers)
    # types_dict = {col: "int" for col in ["left", "top", "width", "height", "right", "bottom"]}
    #
    # print(types_dict)

    field_c_string = "10692017 10712017"
    c_list = [x.strip().split("/") for x in field_c_string.split()]
    for index in range(len(c_list)):
        if len(c_list[index]) == 1:
            c_list[index] = [c_list[index][0][:-4], c_list[index][0][-4:]]
    print(c_list)
def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
