import json
import random


def save_as_json(surface_json: dict):
    filename = 'C:/Users/KosachevIV/PycharmProjects/InputData/layers/lay_name.json'.replace('lay_name', 'lay_name'+str(random.randint(1, 1000)))

    json_file = open(filename, mode='x')
    json.dump(surface_json, json_file)
    json_file.close()

