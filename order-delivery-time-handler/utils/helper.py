import os
import random
from dataclasses import asdict, dataclass
from time import localtime, struct_time
from typing import Any, Dict

import requests
from config.env import load_env
from config.errors import APIConnectionError, DistanceError, WeatherError
from mpu import haversine_distance
from requests.exceptions import ConnectionError
from utils.location import Location
from utils.log import logger
from utils.weather import WeatherApi

JasonObject = Dict[str, Dict[str, Any]]


if "ML_API_URL" not in os.environ:
    load_env()

URL = os.environ["ML_API_URL"]
MONTH_TO_SEASON = {
    12: "winter",
    1: "winter",
    2: "winter",
    3: "spring",
    4: "spring",
    5: "spring",
    6: "summer",
    7: "summer",
    8: "summer",
    9: "fall",
    10: "fall",
    11: "fall",
}

weather_api = WeatherApi()


@dataclass
class RequiredValues:
    distance: str
    current_time: int
    weather: str
    traffic: int
    season: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


def get_estimated_delivery_time_result(required_values: RequiredValues) -> int:
    """
    input : features that need to be trained
    output : predicted estimate time in tuple (hour, minutes)
    """
    try:
        payload = required_values.dict()
        logger.info(f"Querying host {URL} with data: {payload}")
        response_data = requests.post(url=URL, json=payload)

        if response_data.status_code != 200:
            raise APIConnectionError()

        response_data = response_data.json()
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

        user_lat, user_long = user_location.get_lat_and_long()
        restaurant_lat, restaurant_long = restaurant_location.get_lat_and_long()

        if (user_lat, user_long) == (None, None) or (restaurant_lat, restaurant_long) == (None, None):
            raise DistanceError()

        return haversine_distance((user_lat, user_long), (restaurant_lat, restaurant_long))

    except KeyError:
        raise DistanceError()


def get_current_time(time: struct_time) -> int:
    """
    input : struct_time object that contains year, hour, minutes etc..
    output : current time hour * 24 + current time minutes (0 <= current_time <= 24 * 60)
    """
    current_time = time.tm_hour * 60 + time.tm_min

    return current_time


def get_weather() -> str:
    """
    A function for getting the current weather ('cloudy', 'sunny', 'rainy', 'windy')
    """
    try:
        return weather_api.get_current_weather()
    except (ValueError, KeyError, TypeError):
        raise WeatherError()


def get_traffic() -> int:  # TODO: Need to implement
    """
    A function to get current traffic (1 ~ 100)
    """
    return random.randint(1, 100)


def get_season() -> str:
    """
    A function to get current season ('spring', 'summer', 'fall', 'winter')
    """
    current_month = localtime().tm_mon

    return MONTH_TO_SEASON[current_month]
