import json


def parser(file_path: str):
    with open(file_path) as file:
        json_opened = json.load(file)
    return json_opened