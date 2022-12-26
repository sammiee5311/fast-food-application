import argparse
import logging
import os
from typing import Dict

from config.tracing import NotSetTracer, tracer
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask.logging import create_logger
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.trace import Tracer
from utils import get_prediction

load_dotenv(dotenv_path="./config/.env")

OTLP_ENDPOINT = os.environ.get("OTLP_ENDPOINT")

app = Flask(__name__)
logger = create_logger(app)
logger.setLevel(logging.INFO)

if OTLP_ENDPOINT:
    FlaskInstrumentor().instrument_app(app)


@app.route("/predict", methods=["POST"])
def predict() -> Dict[str, str]:
    with tracer.start_as_current_span("predict") as span:
        json_payload = request.json
        logger.info(f"JSON payload: {json_payload}")
        result_payload = get_prediction(json_payload)

        if span.is_recording():
            span.set_attributes(json_payload)
            span.set_attribute("response.prediction", result_payload.get("prediction", None))

        return jsonify(result_payload)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--host", default="0.0.0.0", help="host for flask")
    args.add_argument("--port", default="8080", help="port for flask")

    parsed_args = args.parse_args()

    app.run(parsed_args.host, parsed_args.port, debug=True)
