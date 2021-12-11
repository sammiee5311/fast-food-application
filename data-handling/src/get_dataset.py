from typing import Any, Dict

import pandas as pd
import yaml

CONFIG_YAML = Dict[str, Dict[str, Any]]


def read_params(config_path: str) -> CONFIG_YAML:
    """Read a yaml file that contains config information"""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def get_dataset(config_path: str = "config/params.yaml") -> pd.DataFrame:
    """Get dataset from server which is indicated in config file."""
    config = read_params(config_path)

    data_path = config["data"]["source"]

    df = pd.read_csv(data_path, sep=",", encoding="utf-8")

    return df


if __name__ == "__main__":
    get_dataset()
