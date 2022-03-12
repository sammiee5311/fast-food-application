import os
import pickle
from typing import Any, Dict

import pandas as pd
import yaml
from sklearn.preprocessing import OneHotEncoder

ConfigYaml = Dict[str, Dict[str, Any]]


def save_encoder(encoder_path: str, encoder: OneHotEncoder):
    with open(encoder_path, "wb") as file:
        pickle.dump(encoder, file)


def read_params(config_path: str) -> ConfigYaml:
    """Read a yaml file that contains config information"""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def get_one_hot_encoded_data_frame(df: pd.DataFrame, encoder_path: str) -> pd.DataFrame:
    """Return data frame into one hot encoded and save it"""
    encoder = OneHotEncoder(categories="auto", handle_unknown="ignore")
    encoded_df = pd.DataFrame(encoder.fit_transform(df[["weather", "season"]]).toarray())

    save_encoder(encoder_path, encoder)

    return df.join(encoded_df).drop(columns=["weather", "season"])


def get_dataset(config_path: str = os.path.join("config", "params.yaml")) -> pd.DataFrame:
    """Get dataset from server which is indicated in config file."""
    config = read_params(config_path)

    data_path = config["data"]["source"]
    encoder_path = config["data"]["encoder"]["path"]

    df = pd.read_csv(data_path, sep=",", encoding="utf-8")

    one_hot_encoded_data_frame = get_one_hot_encoded_data_frame(df, encoder_path)

    return one_hot_encoded_data_frame


if __name__ == "__main__":
    get_dataset()
