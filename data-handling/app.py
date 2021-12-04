import argparse
import logging
from typing import Dict

from flask import Flask, jsonify, request
from flask.logging import create_logger

from utils import get_prediction

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route("/predict", methods=["POST"])
def predict() -> Dict[str, str]:
    json_payload = request.json
    LOG.info(f"JSON payload: {json_payload}")
    result_payload = get_prediction(json_payload)

    return jsonify(result_payload)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--host", default="0.0.0.0", help="host for flask")
    args.add_argument("--port", default="8080", help="port for flask")

    parsed_args = args.parse_args()

    app.run(parsed_args.host, parsed_args.port, debug=True)
