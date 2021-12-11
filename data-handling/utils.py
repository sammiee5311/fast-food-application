import json
import os
from typing import Any, Dict

import joblib
import numpy as np
import yaml
from sklearn import linear_model

CONFIG_PATH = os.path.join("config", "params.yaml")
MODEL_PATH = os.path.join("models", "model.joblib")
SCHEMA_PATH = os.path.join("config", "schema.json")
SKLEARN_MODEL = linear_model
JSON_PAYLOAD = Dict[str, Dict[str, Any]]


class DataNotExist(AttributeError):
    def __init__(self, message="Data does not exist. Please Check your data."):
        self.message = message
        super().__init__(self.message)


class FeaturesNotSame(Exception):
    def __init__(self, message="Input is not same as expected model features."):
        self.message = message
        super().__init__(self.message)


class FeaturesNotIncluded(Exception):
    def __init__(self, message="Input is included features that are not in expected model features."):
        self.message = message
        super().__init__(self.message)


def read_params():
    with open(CONFIG_PATH) as yaml_file:
        config = yaml.safe_load(yaml_file)

    return config


def get_model() -> SKLEARN_MODEL:
    # config = read_params()
    # model_path = config["model_path"]
    model = joblib.load(MODEL_PATH)

    return model


def get_schema() -> Dict[str, Dict[str, Any]]:
    with open(SCHEMA_PATH, "r") as file:
        schema = json.load(file)

    del schema["TARGET"]

    return schema


def validate_data(data):
    schema = get_schema()

    if len(data) != len(schema):
        raise FeaturesNotSame

    for col in data.keys():
        if col not in set(schema.keys()):
            raise FeaturesNotIncluded


def get_prediction(data: JSON_PAYLOAD) -> JSON_PAYLOAD:
    try:
        validate_data(data)

        _data = np.array([list(map(float, data.values()))])
        model = get_model()
        prediction = model.predict(_data)

        return dict(prediction=prediction[0])
    except (FeaturesNotSame, FeaturesNotIncluded, ValueError) as error:
        return dict(expected_schema=get_schema(), error=error.args[0])
