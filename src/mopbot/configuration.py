import importlib
import json

import yaml
import jsonschema

from . import data

def load(file):
    # Load configuration file from disk.
    with open(file) as stream:
        return yaml.safe_load(stream)

def validate(config):
    with open(importlib.resources.files(data)/"schema.json") as stream:
        schema = json.load(stream)
    jsonschema.validate(config, schema)
