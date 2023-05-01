import os
import sys
import shutil
import random
import codecs
import pymongo
import argparse
import pdfquery
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from time import sleep

import pdf_parser as pp

import general_methods as gm


def main():
    # print(len("LISTA DE ACUERDOS"))
    # tag = '<LTTextLineHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" word_margin="0.1"><LTTextBoxHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" index="2">No. </LTTextBoxHorizontal></LTTextLineHorizontal>'
    # tag = pp.get_tag_by_attr_position(20, tag)
    # print(tag[-1])
    # tag = '<LTTextBoxHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" index="2">No. </LTTextBoxHorizontal>'
    # tag = pp.get_tag_by_attr_position(20, tag)
    # print(tag[-1])

    in_string = '<LTTextBoxHorizontal y0="818.708" y1="828.668" x0="30.0" x1="46.091" width="16.091" height="9.96" bbox="[30.0, 818.708, 46.091, 828.668]" index="2">No. </LTTextBoxHorizontal>'
    str_find = "Horizontal"
    poses = gm.find_string_indexes(in_string, str_find)
    print(poses)
    print(in_string[poses[0]:poses[1]])


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
