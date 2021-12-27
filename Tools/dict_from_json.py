import json


def dict_from_json(filename: str) -> dict:
    with open(filename) as f:
        return json.load(f)
