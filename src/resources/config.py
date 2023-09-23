import json


def load_configs() -> dict:
    with open("config.json", "r") as config_file:
        configs = json.loads(config_file.read())

    return configs