import os
import yaml


def load_config():
    config_file = "codecollector.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
    return {}
