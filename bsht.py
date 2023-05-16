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

    print(len(all_pdf_paths))
    all_pdf_paths = check_rec_index(all_pdf_paths)
    print(len(all_pdf_paths))


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
