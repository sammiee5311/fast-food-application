import json
import os
import socket
import time
from typing import Any, Dict

from config.db import update_estimated_delivery_time
from config.env import load_env
from config.helper import (
    get_current_time,
    get_distance,
    get_season,
    get_traffic,
    get_weather,
    some_machine_leanring_function,
)
from config.log import logger
from consumer import get_consumer

load_env()

IP_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = os.environ["KAFKA_PORT"]
TOPIC = os.environ["KAFKA_TOPIC"]


JasonObject = Dict[str, Dict[str, Any]]


def predict(data: JasonObject) -> int:
    """
    input : A jason object from web server
    output : predicted estimate time in tuple (hour, minutes)
    """
    try:
        logger.info(
            f"{data['username']!r} ordered {data['menus']} from {data['restaurant_name']!r} at {data['created_on_str']}"
        )
        distance = get_distance(data)
        current_time = get_current_time(time.localtime())
        weather = get_weather()
        traffic = get_traffic()
        season = get_season()
        estimate_time = some_machine_leanring_function(distance, current_time, weather, traffic, season)
        update_estimated_delivery_time(data["id"], estimate_time)
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
