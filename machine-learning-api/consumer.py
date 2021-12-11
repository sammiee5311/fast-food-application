import json
import socket
import time
from dataclasses import dataclass
from time import struct_time
from typing import Any, Dict, List, Optional, Tuple, Union

from kafka import KafkaConsumer
from mpu import haversine_distance
from uszipcode import SearchEngine

IP_ADDRESS = socket.gethostbyname(socket.gethostname())

search = SearchEngine(simple_zipcode=True)

jason_object = Dict[str, Dict[str, Any]]
features_data = List[Union[float, int, str, Tuple[int, int]]]


@dataclass
class Location:
    zipcode: str
    long: Optional[float] = None
    lat: Optional[float] = None

    def set_lat_and_long(self) -> None:
        result = search.by_zipcode(self.zipcode)
        self.long, self.lat = result.lng, result.lat

    def get_lat_and_long(self) -> Tuple[float, float]:
        return self.lat, self.long


def get_distance(data: jason_object) -> float:
    """
    input : A jason object from web server
    output : distance from restaurant location to user location in km
    """
    try:
        user_zipcode, restaraunt_zipcode = data["user_zipcode"], data["restaurant_zipcode"]

        user_location = Location(zipcode=user_zipcode)
        user_location.set_lat_and_long()

        restaurant_location = Location(zipcode=restaraunt_zipcode)
        restaurant_location.set_lat_and_long()

        distance = haversine_distance(user_location.get_lat_and_long(), restaurant_location.get_lat_and_long())

        return distance

    except KeyError as error:
        print(error)


def get_current_time(time: struct_time) -> int:
    """
    input : struct_time object that contains year, hour, minutes etc..
    output : current time hour * 24 + current time minutes (0 <= current_time <= 24 * 60)
    """
    current_time = time.tm_hour * 60 + time.tm_min

    return current_time


def some_machine_leanring_function(features: features_data) -> Tuple[int, int]:
    """
    input : features that need to be trained
    output - predicted estimate time in tuple (hour, minutes)
    """
    return 1, 1


def get_predict(data: jason_object) -> Tuple[int, int]:
    """
    input : A jason object from web server
    output - predicted estimate time in tuple (hour, minutes)
    """
    distance = get_distance(data)
    print(f"distance: {distance: .2f} km")
    current_time = get_current_time(time.localtime())
    print(f"current time: {current_time}")
    # weather = a function for getting the current weather
    # traffic = a function to get current traffic
    # features = [distance, current_time, weather, traffic]
    # estimate_time = some_machine_leanring_function(features)

    return 1, 3


if __name__ == "__main__":
    consumer = KafkaConsumer(
        "fast-food-order",
        security_protocol="PLAINTEXT",
        bootstrap_servers=f"{IP_ADDRESS}:9092",
        auto_offset_reset="earliest",
    )
    print("Starting the comsumer")

    for msg in consumer:
        data = json.loads(msg.value)
        result = get_predict(data)
