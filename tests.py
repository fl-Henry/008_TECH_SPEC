import sys
import random
import requests

from time import sleep, time
from datetime import datetime

# Custom imports
from print_tags import Tags
from app import url_generator, arg_parser, parse_field_c
from general_methods import random_dd_mm_yyy, replace_chars

args = arg_parser()


def tests_url_generator():
    # Tests url_generator
    values_for_url = {
      "capital": [
        "aux1.",
        "aux2.",
        "civ2.",
        "civ3.",
        "civ4.",
        "fam1.",
        "fam2.",
        "fam3.",
        "fam4.",
        "fam5.",
        "mer1.",
        "mer2.",
        "mer3.",
        "mer4.",
        "merOral.",
        "seccc.",
        "seccu.",
        "cjmf1.",
        "cjmf2.",
        "tribl."
      ],
      "lerdo": [
        "Civ1GP.",
        "Civ2GP.",
        "Fam1GP.",
        "Fam2GP.",
        "AuxMixtoGP.",
        "Fam3GP.",
        "secccGP.",
        "seccuGP.",
        "triblG.",
        "Mixto1Lerdo.",
        "Mixto2Lerdo."
      ],
      "foraneos": [
        "canatlan.",
        "nombrededios.",
        "nazas.",
        "cuencame.",
        "sanjuandelrio.",
        "elsalto.",
        "santamariadeloro.",
        "victoria.",
        "santiago."
      ]
    }
    if "01" in args["tests_list"]:
        start_time = datetime.utcnow()
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}\n")
        counter = 0
        test_amount = 10
        for _ in range(test_amount):
            dd, mm, yyyy = random_dd_mm_yyy((1, 1, 2017))
            key_index = random.randint(0, 2)
            key = [*values_for_url.keys()][key_index]
            value_index = random.randint(0, len([*values_for_url.keys()][0]) - 1)
            value = values_for_url[key][value_index]
            print("day:", dd, ", mm: ", mm, ", yyyy: ", yyyy, ", key: ", key, ", value: ", value)
            url = url_generator((dd, mm, yyyy), value)
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


def tests_replace_chars():
    if "02" in args["tests_list"]:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        string_for_checking = "Dictados el día jueves 27 de abril de 2023"
        result_string = "DICTADOS EL DIA JUEVES 27 DE ABRIL DE 2023"
        string_temp = string_for_checking
        print(f"string_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking)
        print(f"string_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking).upper()
        print(f"string_temp: {string_temp}")
        if result_string == string_temp:
            print("Match")
            counter += 1
        else:
            raise AssertionError

        string_for_checking = "áéíóöúüÁÉÍÓÖÚÜ"
        result_string = "AEIOOUUAEIOOUU"
        string_temp = string_for_checking
        print(f"\nstring_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking)
        print(f"string_temp: {string_temp}")
        string_temp = replace_chars(string_for_checking).upper()
        print(f"string_temp: {string_temp}")
        if result_string == string_temp:
            print("Match")
            counter += 1
        else:
            raise AssertionError

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in args["tests_list"]:
            sys.exit(0)


def tests_parce_field_c():
    if "02" in args["tests_list"]:
        start_time = datetime.utcnow()
        counter = 0
        print(f"\n{Tags.Blue}======= TIMESTAMP UTC ======= {datetime.utcnow()} ======={Tags.ResetAll}")

        c_fields = [
            "007CC/2016 1149/2017 0333/2010 ",
            "1149/2017 0333/2010 007CC/2016",
            "0333/2010 1149/2017 007CC/2016",
        ]
        for c_field in c_fields:
            res = parse_field_c(c_field)
            print(res)

        end_time = datetime.utcnow()
        work_time = end_time - start_time
        print("\nWorking time of the test:", work_time)
        print(f"Test completed: {counter}/{2} is done")
        if "EAT" in args["tests_list"]:
            sys.exit(0)



if __name__ == '__main__':
    tests_url_generator()
    tests_replace_chars()
    tests_parce_field_c()
