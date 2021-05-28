# __Author__: Khoi Van 2021

import argparse
import csv
import logging
import re
# import shutil
import sys
# from functools import partial
# from itertools import groupby
# from multiprocessing import Pool
# from operator import itemgetter
from pathlib import Path, PurePath
from typing import Dict, List, Optional, Union

# from fuzzywuzzy import fuzz, process
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeElapsedColumn

console = Console()
sys.setrecursionlimit(20000)

# Set logger using Rich: https://rich.readthedocs.io/en/latest/logging.html
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")


CURRENT_FILEPATH = Path(__file__).resolve().parent
DATA_FOLDER = CURRENT_FILEPATH / 'data'
DATA_FOLDER.mkdir(exist_ok=True)
INPUT_FILE = DATA_FOLDER / 'ncfCatalogIdSwitch.xml'
DIRECTORY_FILE = DATA_FOLDER / 'productIdDirectory.csv'
OUTPUT_FILE = DATA_FOLDER / 'ncfCatalogIdSwitch-fixed.xml'

INPUT_MANUAL_FOLDER = DATA_FOLDER / 'manuals'
OUTPUT_MANUAL_FOLDER = CURRENT_FILEPATH.parent / 'manuals'

LOG_FOLDER = CURRENT_FILEPATH / 'logs'
LOG_FOLDER.mkdir(exist_ok=True)
FOUND_MANUALS_RESULT_FILE = LOG_FOLDER / 'found_manuals.csv'
NOT_FOUND_MANUALS_RESULT_FILE = LOG_FOLDER / 'not_found_manuals.csv'


def init_argparse() -> argparse.ArgumentParser:
    """Creating CLI helper"""
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [OPTIONS]",
        description="Generate Installation Manuals for North Country Fire items."
    )
    parser.add_argument('-d', '--debug',
                        help='Print more debug info.',
                        action="store_true")
    parser.add_argument('-p', '--parallel',
                        help='Generate Installation Manual files in asynchronous fashion (default).',
                        default=True,
                        action="store_true")
    parser.add_argument('-s', '--sequential',
                        help='Generate Installation Manual files sequentially.',
                        action="store_true")
    return parser


def load_directory_file(file: PurePath) -> Dict[str, str]:
    with open(file, 'r', newline='') as csv_file:
        dict_reader = csv.DictReader(csv_file)
        # return {line['oldID']: line['newID']
        #         for line in dict_reader}
        # return ((line['oldID'], line['newID'])
        #         for line in dict_reader)
        for line in dict_reader:
            yield (line['oldID'], line['newID'])


def replace_product_id(input_file: PurePath,
                       directory_file: PurePath,
                       output_file: PurePath) -> None:
    product_id_directory = load_directory_file(directory_file)

    with open(input_file, 'r') as f_in:
        content = f_in.read()

    # breakpoint()

    # for old_id, new_id in product_id_directory.items():
    # for i, directory_item in enumerate(product_id_directory):
    for i, (old_id, new_id) in enumerate(product_id_directory):
        # content = re.sub(rf'''(?<=product-id=(?:\"|\')){old_id}(?=(?:\"|\'))''', new_id, content)

        # old_id, new_id = directory_item
        # breakpoint()
        if i % 100 == 0:
            console.log(f'Directory line: {i}')
            console.log(f'Replacing {old_id}')
        content = re.sub(rf'''
                              (?<!https://www\.northcountryfire\.com/products/)
                              {old_id}
                         ''',
                         new_id,
                         content, flags=re.VERBOSE)

    with open(output_file, 'w') as f_out:
        f_out.write(content)


if __name__ == '__main__':
    parser = init_argparse()
    debug = parser.parse_args().debug
    parallel = parser.parse_args().parallel
    sequential = parser.parse_args().sequential
    parsing_mode = 'sequential' if sequential else 'parallel'

    if debug:
        replace_product_id(input_file=INPUT_FILE,
                            directory_file=DIRECTORY_FILE,
                            output_file=OUTPUT_FILE)

    else:
        # # Use Python Rich Progress
        # Ref: https://github.com/willmcgugan/rich/issues/121
        progress = Progress(SpinnerColumn(),
                            "[bold green]{task.description}",
                            # BarColumn(),
                            # "[progress.percentage]{task.percentage:>3.1f}%",
                            # "({task.completed} of {task.total})"
                            "•",
                            TimeElapsedColumn(),
                            # transient=True,
                            # start=False,
                            console=console)

        with progress:
            # progress.log(f'Scraping images from Napoleon catalog')
            task_description = f'Replacing old product-id ...'
            task_id = progress.add_task(task_description, start=False)

            try:
                progress.start_task(task_id)
                replace_product_id(input_file=INPUT_FILE,
                                directory_file=DIRECTORY_FILE,
                                output_file=OUTPUT_FILE)

            except Exception as error:
                # if debug:
                # traceback_str = ''.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
                # log.error(traceback_str)
                log.exception(error)
                # console.log(error)
