import importlib
import json
import logging

import yaml
import jsonschema

from . import data

logger = logging.getLogger(__name__)

def load(file) -> dict:
    """Load the specified configuration file from disk."""
    logger.info(f"Loading config file: {file}")
    with open(file) as stream:
        return yaml.safe_load(stream)

def validate(config) -> None:
    logger.debug("Loading JSON Schema for config validation.")
    with open(importlib.resources.files(data)/"schema.json") as stream:
        schema = json.load(stream)

    jsonschema.validate(config, schema)
    logger.info("Config file successfully validated")
