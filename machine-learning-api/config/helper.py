import os
from time import struct_time
from typing import Any, Dict

import requests
from mpu import haversine_distance
from requests.exceptions import ConnectionError

from config.env import load_env
from config.errors import APIConnectionError, DistanceError, WeatherError
from config.location import Location
from config.log import logger

JasonObject = Dict[str, Dict[str, Any]]

if "ML_API_URL" not in os.environ:
    load_env()

URL = os.environ["ML_API_URL"]


def some_machine_leanring_function(distance, current_time, weather, traffic, season) -> int:
    """
    input : features that need to be trained
    output : predicted estimate time in tuple (hour, minutes)
    """
    try:
        payload = dict(distance=distance, current_time=current_time, weather=weather, traffic=traffic, season=season)
        logger.info(f"Querying host {URL} with data: {payload}")
        response_data = requests.post(url=URL, json=payload).json()

        predicted_time = response_data["prediction"]

        return predicted_time
    except ConnectionError:
        raise APIConnectionError()


def get_distance(data: JasonObject) -> float:
    """
    input : A json object from web server
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


def get_weather() -> str:  # TODO: Need to implement
    """
    A function for getting the current weather ('cloudy', 'sunny', 'rainy', 'windy')
    """
    try:
        return "sunny"
    except (ValueError, KeyError, TypeError):
        raise WeatherError()


def get_traffic() -> int:  # TODO: Need to implement
    """
    A function to get current traffic (1 ~ 100)
    """
    return 10


def get_season() -> str:  # TODO: Need to implement
    """
    A function to get current season ('spring', 'summer', 'fall', 'winter')
    """
    return "summer"
