import logging
from typing import Dict

import click
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


@click.command("flask")
@click.option("--host", default="0.0.0.0", help="host")
@click.option("--port", default="8080", help="port")
def main(host: str, port: str):
    app.run(host, port, debug=True)


if __name__ == "__main__":
    main()
