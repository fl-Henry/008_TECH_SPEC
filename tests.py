import sys
import random
import requests

from time import sleep, time
from datetime import datetime

from app import url_generator, arg_parser
from general_methods import random_dd_mm_yyy

args = arg_parser()


def tests_url_generator(values_for_url):
    # Tests url_generator
    if "01" in args["tests_list"]:
        start_time = datetime.utcnow()
        print(f"\n======= TIMESTAMP UTC ======= {datetime.utcnow()} =======\n")
        counter = 0
        test_amount = 10
        for _ in range(test_amount):
            dd, mm, yyyy = random_dd_mm_yyy((1, 1, 2017))
            key_index = random.randint(0, 2)
            key = [*values_for_url.keys()][key_index]
            value_index = random.randint(0, len([*values_for_url.keys()][0]) - 1)
            value = values_for_url[key][value_index]
            print("day:", dd, ", mm: ", mm, ", yyyy: ", yyyy, ", key: ", key, ", value: ", value)
            url = url_generator(dd, mm, yyyy, value)
            print(url)
            response_ = requests.get(url)
            if response_.text == "Not Found [CFN #0005]":
                print(response_.text)
            else:
                print("File Exists")
                counter += 1
            sleep(0.2)
            print()
        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("Working time of the test:", work_time)
        print(f"Test completed: {counter}/{test_amount} files exist")
        if "EAT" in args["tests_list"]:
            sys.exit(0)

