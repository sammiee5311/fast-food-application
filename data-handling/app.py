import logging
from typing import Any, Dict

import click
import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask.logging import create_logger

CONFIG_PATH = "params.yaml"
MODEL_PATH = "model.joblib"

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


def get_model():
    model = joblib.load(MODEL_PATH)

    return model


def get_prediction(data: Dict[str, Dict[str, Any]]) -> str:
    _data = np.array([list(map(float, data.values()))])

    model = get_model()
    prediction = model.predict(_data)

    return prediction[0]


@app.route("/predict", methods=["POST"])
def predict() -> Dict[str, str]:
    json_payload = request.json
    LOG.info(f"JSON payload: {json_payload}")
    prediction = get_prediction(json_payload)

    return jsonify({"prediction": prediction})


@click.command("flask")
@click.option("--host", default="0.0.0.0", help="host")
@click.option("--port", default="8080", help="port")
def main(host: str, port: str):
    app.run(host, port, debug=True)


if __name__ == "__main__":
    main()
