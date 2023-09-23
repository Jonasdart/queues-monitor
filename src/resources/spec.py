import json


def load_spec() -> dict:
    with open("queues.spec", "r") as spec_file:
        spec = json.loads(spec_file.read())

    return spec