import json
from dotmap import DotMap

class Config:
    @staticmethod
    def initialize(filepath):
        with open(filepath) as f:
            settings = DotMap(json.loads(f.read()))
            return settings

