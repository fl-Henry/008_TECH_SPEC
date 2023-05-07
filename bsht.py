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
    types_dict = {col: "int" for col in ["left", "top", "width", "height", "right", "bottom"]}

    print(types_dict)


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    main()
