import json
from dotmap import DotMap
from local_libs.winregistry import Registry


class Config:
    def __init__(self, winreg_key):
        self.registry = Registry(winreg_key)

    # def __call__(self, *args, **kwargs):
    #     return self.get()

    def get(self):
        return DotMap(json.loads(self.registry.get_value("config")))

    def set(self, new_value):
        self.registry.set_value("config", json.dumps(new_value))


def parse_config(filepath):
    with open(filepath) as f:
        return json.dumps(json.load(f), indent=0).replace("\n", "").replace(" ", "")


# class Config:
#     @staticmethod
#     def initialize(winreg_key):
#         WINREG = Registry(winreg_key)
#         settings = DotMap(json.loads(WINREG.get_value("config")))
#         return settings
#
#     @staticmethod
#     def update(winreg_key, new_value):
#         WINREG = Registry(winreg_key)
#         WINREG.set_value("config", new_value)
#
#     @staticmethod
#     def initialize(filepath):
#         with open(filepath) as f:
#             settings = DotMap(json.loads(f.read()))
#             return settings
#
#     def get(self):
#         pass
#
#     def update(self, new_value):
#         pass
