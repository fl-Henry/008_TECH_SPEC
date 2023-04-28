import os
import sys
import random
import shutil
import argparse

from datetime import datetime, timedelta

# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


class DaNHandler:

    def __init__(self):
        base_path = str(__file__)[:len(__file__) - len(os.path.basename(str(__file__))) - 1]
        base_dir = f"{base_path}/"
        temp_dir = f"{base_dir}temp/"
        for_tests_dir = f"{temp_dir}for_tests/"

        self.dirs = {
            "base_dir": base_dir,
            "temp_dir": temp_dir,
            "for_tests_dir": for_tests_dir,
        }

        self.dirs_to_remove = {
            "temp_dir": temp_dir,
        }

        self.files = {

        }

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
        # parser.add_argument('--second-symbol', dest='second_symbol', default='USDT',
        #                     help='Symbol of token as money Ex: "USDT"')
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

        # Output of arguments
        stdout = f"\ntests: {args['tests_list']}"
        args.update({"stdout": stdout})

        return args

    except Exception as _ex:
        print("[ERROR] Parsing arguments >", _ex)
        sys.exit(1)


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
