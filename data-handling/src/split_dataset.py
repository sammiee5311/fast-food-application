import os
from typing import Any, Dict, Tuple

import click
import pandas as pd
from sklearn.model_selection import train_test_split

from get_dataset import read_params

ConfigYaml = Dict[str, Dict[str, Any]]
TrainDataInfo = Tuple[str, str, str, str, str]


def get_information(config: ConfigYaml) -> TrainDataInfo:
    """Get information for splitting dataset into train and test"""
    train_data_path = config["data"]["train"]["path"]
    test_data_path = config["data"]["test"]["path"]
    raw_data_path = config["data"]["raw"]["path"]
    test_size = config["data"]["test"]["size"]
    random_state = config["data"]["train"]["random_state"]

    return train_data_path, test_data_path, raw_data_path, test_size, random_state


@click.command("get")
@click.option("--config_path", default=os.path.join("config", "params.yaml"), help="Config path")
def split_dataset(config_path: str):
    """Split dataset into test and train dataset as csv files."""
    config = read_params(config_path)
    train_data_path, test_data_path, raw_data_path, test_size, random_state = get_information(config)

    data = pd.read_csv(raw_data_path, sep=",")
    train, test = train_test_split(data, test_size=test_size, random_state=random_state)
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")


if __name__ == "__main__":
    split_dataset()
