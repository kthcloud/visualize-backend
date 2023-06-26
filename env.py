import json


def read_env(env):
    with open("/etc/visualize/config/config.json", "r+") as file:
        return json.loads(file.read())[env]
    return None
