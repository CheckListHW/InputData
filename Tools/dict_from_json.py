import json


def dict_from_json(filename: str) -> dict:
    print(filename)
    with open(filename) as f:
        return json.load(f)
