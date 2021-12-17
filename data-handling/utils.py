import json
import os
import pickle
from enum import Enum
from typing import Any, Dict, List, Union

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn import linear_model
from sklearn.preprocessing import OneHotEncoder

from config.errors import FeatureDataError, FeaturesNotIncluded, FeaturesNotSame
from config.feature_data import Features, Season, Weather

CONFIG_PATH = os.path.join("config", "params.yaml")
SCHEMA_PATH = os.path.join("config", "schema.json")

ConfigYaml = Dict[str, Dict[str, Any]]
Schema = Dict[str, Dict[str, Any]]
SklearnModel = linear_model
JsonPayload = Dict[str, Dict[str, Any]]


def read_params() -> ConfigYaml:
    """Read a yaml file that contains config information"""
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    return config


def get_schema() -> Schema:
    with open(SCHEMA_PATH, "r") as file:
        schema = json.load(file)

    return schema


def get_model() -> SklearnModel:
    config = read_params()
    model_path = config["api_model_path"]
    model = joblib.load(model_path)

    return model


def save_encoder(encoder_path: str, encoder: OneHotEncoder):
    with open(encoder_path, "wb") as file:
        pickle.dump(encoder, file)


def load_encoder() -> OneHotEncoder:
    config = read_params()
    encoder_path = config["data"]["encoder"]["path"]
    with open(encoder_path, "rb") as file:
        encoder = pickle.load(file)

    return encoder


def get_features_payload(data: Union[List[str], JsonPayload], server=False) -> JsonPayload:
    distance = current_time = weather = traffic = season = None
    if isinstance(data, list):
        distance, current_time, weather, traffic, season = data
    else:
        for key, val in data.items():
            if key == "distance":
                distance = val
            elif key == "current_time":
                current_time = val
            elif key == "weather":
                weather = val
            elif key == "traffic":
                traffic = val
            else:
                season = val

    features = Features(
        distance=distance, current_time=current_time, weather=Weather(weather), traffic=traffic, season=Season(season)
    )

    payload = {}

    for key, val in features:
        if isinstance(val, Enum):
            payload[key] = [val.value] if server else val.value
        else:
            payload[key] = [val] if server else val

    return payload


def get_trainable_date(data) -> np.array:
    encoder = load_encoder()
    test_data = pd.DataFrame.from_dict(data)
    d = np.array([data["distance"][-1], data["current_time"][-1], data["traffic"][-1]])

    encoded_test_data = pd.DataFrame(encoder.transform(test_data[["weather", "season"]]).toarray())
    trainable_data = np.concatenate(([d], encoded_test_data.values), axis=1)

    return trainable_data


def validate_data(data) -> None:
    schema = get_schema()["required"]
    features = get_features_payload(data, server=True)

    if len(features) != len(schema):
        raise FeaturesNotSame

    for col in features.keys():
        if col not in set(schema):
            raise FeaturesNotIncluded

    return features


def get_prediction(data: JsonPayload) -> JsonPayload:
    try:
        data = validate_data(data)

        data = get_trainable_date(data)

        model = get_model()
        prediction = model.predict(data)

        return dict(prediction=prediction[0])
    except (FeaturesNotSame, FeaturesNotIncluded, ValueError, FeatureDataError) as error:
        error_message = error.args[0]
        if isinstance(error_message, list):
            error_message = {}
            for err in error.args[0]:
                error_message[err._loc] = str(err.exc)

        return dict(expected_schema=get_schema(), error=error_message)
