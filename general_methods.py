import os
import sys
import random
import shutil
import argparse

from datetime import datetime, timedelta, date

# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


class DaNHandler:

    def __init__(self):
        base_path = str(__file__)[:len(__file__) - len(os.path.basename(str(__file__))) - 1]
        base_dir = f"{base_path}/"
        temp_dir = f"{base_dir}temp/"
        for_tests_dir = f"{base_dir}for_tests/"

        self.dirs = {
            "base_dir": base_dir,
            "temp_dir": temp_dir,
            "for_tests_dir": for_tests_dir,
            "capital": f"{temp_dir}capital/",
            "lerdo": f"{temp_dir}lerdo/",
            "foraneos": f"{temp_dir}foraneos/",
        }

        self.dirs_to_remove = {
            "temp_dir": temp_dir,
            "for_tests_dir": for_tests_dir,
        }

        self.files = {}
        self.create_dirs()

    def __str__(self):
        stdout = ""

        # Add dirs in stdout
        if len(self.dirs) > 0:
            stdout = f"\nDirs: "
            for key in self.dirs.keys():
                stdout += f"\n  {key:<16}: {self.dirs[key]}"

        # Add files in stdout
        if len(self.files) > 0:
            stdout += f"\nFiles: "
            for key in self.files.keys():
                stdout += f"\n  {key:<16}: {self.files[key]}"

        # Add dirs_to_delete in stdout
        if len(self.dirs_to_remove) > 0:
            stdout += f"\nDirs to delete: "
            for key in self.dirs_to_remove.keys():
                stdout += f"\n  {key:<16}: {self.dirs_to_remove[key]}"

        return stdout

    # Create all dirs
    def create_dirs(self):
        for key in self.dirs.keys():
            if not os.path.exists(self.dirs[key]):
                os.mkdir(self.dirs[key])

    # Delete all dirs
    def remove_dirs(self):
        for key in self.dirs_to_remove.keys():
            if os.path.exists(self.dirs_to_remove[key]):
                shutil.rmtree(self.dirs_to_remove[key], ignore_errors=True)


def arg_parser():
    # Parsing of arguments
    try:
        parser = argparse.ArgumentParser(description='TECH_SPEC')
        parser.add_argument('--tests', dest='tests_str', default=None,
                            help='Names of testes // separator "-"; Ex: "01-02-03"')
        parser.add_argument('--start-date', dest='start_date', default='1-1-2023',
                            help='Which date is scraping starts from // dd-mm-yyyy; Ex: "31-12-2022"')
        parser.add_argument('--end-date', dest='end_date', default=None,
                            help='Which date is scraping ends to // dd-mm-yyyy; Ex: "31-12-2022"')
        # parser.add_argument('--id', dest='id', default=5,
        #                     help='Id of callback Ex: 5')
        # parser.add_argument('--test', dest='test_key', nargs='?', const=True, default=False,
        #                     help='Enable test mode')
        # parser.add_argument('--force-url', dest='force_url', nargs='?', const=True, default=False,
        #                     help="Enable force url for Spot and Websocket (in the test mode has no effect")
        parsed_args = parser.parse_args()

        # Arguments
        args = {}
        args.update({"tests_list": str(parsed_args.tests_str).split("-")})
        args.update({"start_date": [int(x) for x in str(parsed_args.start_date).split("-")]})
        if parsed_args.end_date is None:
            parsed_args.end_date = datetime.today().strftime("%d-%m-%Y")
        args.update({"end_date": [int(x) for x in str(parsed_args.end_date).split("-")]})

        # Output of arguments
        stdout = "\nArguments: "
        if len(args) > 0:
            for key in args.keys():
                stdout += f"\n{key:<16}: {args[key]}"

        args.update({"stdout": stdout})

        return args

    except Exception as _ex:
        print("[ERROR] Parsing arguments >", _ex)
        sys.exit(1)


def delete_last_print_lines(n=1):
    # print("Entering to loop")
    # delete_last_print_lines()
    # print(f"{list_index}/{len(symbols_list)}")
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


# # ===== String Methods ========================================================================= String Methods =====
...
# # ===== String Methods ========================================================================= String Methods =====


def replace_chars(in_str):
    # TODO: Transform 'áéíóöúüÁÉÍÓÖÚÜ' to 'aeioouuAEIOOUU'
    """"""

    # Char set for replace
    char_set = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ö": "o",
        "ú": "u",
        "ü": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ö": "O",
        "Ú": "U",
        "Ü": "U",
    }

    out_str = ''
    for char in in_str:
        if char in [*char_set.keys()]:
            char = char_set[char]
        out_str += char
    return out_str


def url_to_name(file_url, iter_count=1):
    input_file_url = file_url
    file_name = file_url
    process_url = file_url
    error_counter = 0
    while iter_count > 0:

        # Checking infinite loop
        error_counter += 1
        if error_counter > 8000:
            print("[ERROR] url_to_name > infinite loop")
            print(input_file_url)
            raise LookupError

        # Method logic
        if process_url[-1] == '/':
            process_url = process_url[:-1]
        for _ in range(1, len(process_url)):
            char = process_url[-1]
            if char == '/':
                file_name = file_url[len(process_url):]
                file_url = process_url[:-1]
                iter_count -= 1
                break
            else:
                process_url = process_url[:-1]
    return file_name


def url_parent(file_url, iter_count=1):
    input_file_url = file_url
    parent_url = file_url
    process_url = file_url
    error_counter = 0
    while iter_count > 0:

        # Checking infinite loop
        error_counter += 1
        if error_counter > 8000:
            print("[ERROR] url_parent > infinite loop")
            print(input_file_url)
            raise LookupError

        # Method logic
        if process_url[-1] == '/':
            process_url = process_url[:-1]
        for _ in range(1, len(process_url)):
            char = process_url[-1]
            if char == '/':
                parent_url = process_url
                iter_count -= 1
                break
            else:
                process_url = process_url[:-1]

    return parent_url


# # ===== Date Methods ============================================================================= Date Methods =====
...
# # ===== Date Methods ============================================================================= Date Methods =====


def dates_between(start_date, end_date):
    """
    :param start_date: tuple[int, int, int]     | (31, 12, 2023)
    :param end_date: tuple[int, int, int]       | (31, 12, 2023)
    :return: list[tuple[int, int, int]]
    """
    start_date = date(start_date[2], start_date[1], start_date[0])
    end_date = date(end_date[2], end_date[1], end_date[0])

    delta = end_date - start_date

    dates_between_list = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates_between_list.append([int(x) for x in str(day.strftime("%d-%m-%Y")).split("-")])

    return dates_between_list


def random_dd_mm_yyy(start_date, end_date: tuple[int, int, int] = None):
    if end_date is None:
        end_date = datetime.today()
    else:
        if len(end_date) == 3:
            end_date = datetime(year=end_date[2], month=end_date[1], day=end_date[0])
        else:
            raise ValueError
    start_date = datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    dd = int(str(random_date.strftime("%d")))
    mm = int(str(random_date.strftime("%m")))
    yyyy = int(str(random_date.strftime("%Y")))
    return dd, mm, yyyy
