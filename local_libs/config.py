import json
from local_libs.winregistry import Registry
# from winregistry import Registry


class Config:
    def __init__(self, winreg_key):
        self.registry = Registry(winreg_key)

    def get(self):
        return json.loads(json.loads(self.registry.get_value("config")))

    def set(self, new_value):
        self.registry.set_value("config", json.dumps(new_value))

    def __getattr__(self, item):
        return self.get()[item]


def parse_config(filepath):
    with open(filepath) as f:
        return json.dumps(json.load(f), indent=0).replace("\n", "").replace(" ", "")


# config = Config("MALWARE")
# print(config.master_server)
