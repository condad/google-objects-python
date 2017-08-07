import os
import json


def get_data(file_name):
    path = os.path.join('./tests/data', file_name + '.json')
    path = os.path.abspath(path)

    with open(path) as fl:
        data = json.load(fl)

    return data
