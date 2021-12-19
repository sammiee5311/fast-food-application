import os
from time import struct_time
from typing import Any, Dict, Tuple

import requests
from mpu import haversine_distance
from requests.exceptions import ConnectionError

from config.location import Location
from config.log import logger

JasonObject = Dict[str, Dict[str, Any]]

URL = os.environ["ML_API_URL"]


class DistanceError(Exception):
    def __init__(self, message="an error while calculating distance"):
        self.message = message
        super().__init__(self.message)


class WeatherError(Exception):
    def __init__(self, message="an error while getting weather info"):
        self.message = message
        super().__init__(self.message)


class APIConnectionError(Exception):
    def __init__(self, message="machine learning api cannot be connected"):
        self.message = message
        super().__init__(self.message)


def some_machine_leanring_function(distance, current_time, weather, traffic, season) -> Tuple[int, int]:
    """
    input : features that need to be trained
    output : predicted estimate time in tuple (hour, minutes)
    """
    try:
        payload = dict(distance=distance, current_time=current_time, weather=weather, traffic=traffic, season=season)
        logger.info(f"Querying host {URL} with data: {payload}")
        response_data = requests.post(url=URL, json=payload).json()

        predicted_time = response_data["prediction"]

        hour, min = predicted_time // 60, predicted_time % 60

        return hour, min
    except ConnectionError:
        raise APIConnectionError()


def get_distance(data: JasonObject) -> float:
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

        if user_location.get_lat_and_long() == (None, None) or restaurant_location.get_lat_and_long() == (None, None):
            raise DistanceError()

        distance = haversine_distance(user_location.get_lat_and_long(), restaurant_location.get_lat_and_long())
        return distance

    except KeyError:
        raise DistanceError()


def get_current_time(time: struct_time) -> int:
    """
    input : struct_time object that contains year, hour, minutes etc..
    output : current time hour * 24 + current time minutes (0 <= current_time <= 24 * 60)
    """
    current_time = time.tm_hour * 60 + time.tm_min

    return current_time


def get_weather() -> str:  # Need to implement
    """
    A function for getting the current weather ('cloudy', 'sunny', 'rainy', 'windy')
    """
    try:
        """do function"""

        return "sunny"
    except:
        raise WeatherError()


def get_traffic() -> int:  # Need to implement
    """
    A function to get current traffic (1 ~ 100)
    """
    return 10


def get_season() -> str:  # Need to implement
    """
    A function to get current season ('spring', 'summer', 'fall', 'winter')
    """
    return "summer"
