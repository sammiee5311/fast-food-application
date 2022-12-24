import argparse
import logging
import os
from typing import Dict

from config.tracing import NotSetTracer, enable_open_telemetry
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask.logging import create_logger
from opentelemetry.trace import Tracer
from utils import get_prediction

load_dotenv(dotenv_path="./config/.env")

OTLP_ENDPOINT = os.environ.get("OTLP_ENDPOINT")

app = Flask(__name__)
logger = create_logger(app)
logger.setLevel(logging.INFO)
tracer: Tracer | NotSetTracer = NotSetTracer()

if not OTLP_ENDPOINT:
    tracer = enable_open_telemetry(app, OTLP_ENDPOINT)


@app.route("/predict", methods=["POST"])
def predict() -> Dict[str, str]:
    json_payload = request.json
    logger.info(f"JSON payload: {json_payload}")
    result_payload = get_prediction(json_payload)

    return jsonify(result_payload)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--host", default="0.0.0.0", help="host for flask")
    args.add_argument("--port", default="8080", help="port for flask")

    parsed_args = args.parse_args()

    app.run(parsed_args.host, parsed_args.port, debug=True)
