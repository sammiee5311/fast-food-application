import os
from typing import Any, Dict

import joblib
import numpy as np
from sklearn import linear_model

CONFIG_PATH = os.path.join("config", "params.yaml")
MODEL_PATH = os.path.join("models", "model.joblib")
SKLEARN_MODEL = linear_model


def get_model() -> SKLEARN_MODEL:
    model = joblib.load(MODEL_PATH)

    return model


def get_prediction(data: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    _data = np.array([list(map(float, data.values()))])

    model = get_model()

    try:
        prediction = model.predict(_data)
        return dict(prediction=prediction[0])
    except ValueError as error:
        return dict(error=error.args)
