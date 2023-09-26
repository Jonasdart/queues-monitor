import json
import os
from dotenv import load_dotenv

if os.environ.get("environ_name") != "prod":
    load_dotenv()


def load_configs() -> dict:
    with open("config.json", "r") as config_file:
        configs = json.loads(config_file.read())

    return configs