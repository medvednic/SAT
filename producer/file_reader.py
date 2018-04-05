import json


def read_json(file_name):
    with open('config/' + file_name, encoding="utf-8") as f:
        return json.load(f)