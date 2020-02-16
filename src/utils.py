import argparse
import re

from typing import List
from bs4 import BeautifulSoup


def get_program_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("html_file_path")

    return parser.parse_args()


def get_data_from_html(html_file_path: str) -> List:
    with open(html_file_path, 'r') as html_file:
        bs = BeautifulSoup(html_file, features='html')

    data = bs.get_text(separator='~!@#')

    normalized_data_list = []
    for unnormalized_item in data.split('~!@#'):
        for normalized_item in re.split(r':|=|[ ]|Â', unnormalized_item):
            normalized_item = normalized_item.strip()
            normalized_data_list.append(normalized_item)

    return list(filter(data_filter, normalized_data_list))


def data_filter(item) -> bool:
    return item not in (
        '\n',
        ',',
        '',
        ' ',
        ':'
    )
