import json
import os
import time
from typing import Any, Dict

from config.env import load_env
from consumer import get_consumer
from utils.db import PostgreSQL, update_estimated_delivery_time
from utils.helper import (
    RequiredValues,
    get_current_time,
    get_distance,
    get_estimated_delivery_time_result,
    get_season,
    get_traffic,
    get_weather,
)
from utils.log import logger
from utils.tracing import tracer

load_env()

IP_ADDRESS = "kafka"
PORT = os.environ["KAFKA_PORT"]
TOPIC = os.environ["KAFKA_TOPIC"]
DATABASE = PostgreSQL
OTLP_ENDPOINT = os.environ.get("OTLP_ENDPOINT")


JasonObject = Dict[str, Dict[str, Any]]


@tracer.start_as_current_span("predict")
def predict(data: JasonObject) -> int:
    """
    input : A jason object from web server
    output : predicted estimate time in tuple (hour, minutes)
    """
    try:
        logger.info(
            f"{data['username']!r} ordered {data['menus']} from {data['restaurant_name']!r} at {data['created_on_str']}"
        )
        required_values = RequiredValues(
            distance=get_distance(data),
            current_time=get_current_time(time.localtime()),
            weather=get_weather(),
            traffic=get_traffic(),
            season=get_season(),
        )
        estimate_time = get_estimated_delivery_time_result(required_values)
        update_estimated_delivery_time(DATABASE, data["id"], estimate_time)  # TODO: Need to seperate
    except Exception as error:  # TODO: Need to modify
        logger.warning(f"An error occured : {error}")
        return 0

    return estimate_time


if __name__ == "__main__":
    consumer = get_consumer(TOPIC, IP_ADDRESS, PORT)

    for msg in consumer:
        data = json.loads(msg.value)
        result = predict(data)
        logger.info(f"Result : {result}")
