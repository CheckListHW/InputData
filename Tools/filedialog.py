import json
import random

import os


def save_as_json(data: dict, path: str = os.getcwd(), filename: str = 'lay_name' + str(random.randint(1, 1000))):
    filename = path + '/lay_name.json'.replace('lay_name', filename)
    filename.replace('//', '/')

    try:
        json_file = open(filename, mode='x')
        json.dump(data, json_file)
        json_file.close()
    except:
        print('save_as_json')
        return None

    return filename

