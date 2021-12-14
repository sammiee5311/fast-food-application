import json
import socket
import time
from typing import Any, Dict, List, Tuple, Union

from kafka import KafkaConsumer

from config.helper import (
    get_current_time,
    get_distance,
    get_season,
    get_traffic,
    get_weather,
    some_machine_leanring_function,
)
from config.log import logger

IP_ADDRESS = socket.gethostbyname(socket.gethostname())


JasonObject = Dict[str, Dict[str, Any]]
Features = List[Union[float, int, str, Tuple[int, int]]]


def predict(data: JasonObject) -> Tuple[int, int]:
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
    except Exception as error:  # Need to modify
        logger.warning(f"An error occured : {error}")
        return 0

    return estimate_time


if __name__ == "__main__":
    consumer = KafkaConsumer(
        "fast-food-order",
        security_protocol="PLAINTEXT",
        bootstrap_servers=f"{IP_ADDRESS}:9092",
        auto_offset_reset="earliest",
    )
    logger.info("Starting the comsumer")

    for msg in consumer:
        data = json.loads(msg.value)
        result = predict(data)
        logger.info(f"Result : {result}")
