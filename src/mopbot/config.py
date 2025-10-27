import importlib
import json

import yaml
import jsonschema

from . import data

config = []

# Load configuration file from disk.
with open("config.yaml") as stream:
    config = yaml.safe_load(stream);

def validate(config):
    with open(importlib.resources.files(data)/"schema.json") as stream:
        schema = json.load(stream)
    jsonschema.validate(config, schema)
