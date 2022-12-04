import json
import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

import requests
from config.env import load_env

if "WEATHER_API_KEY" not in os.environ:
    load_env()

CONDITIONS = {
    "cloudy": ["clouds", "mist", "smoke", "haze", "dust", "fog", "sand", "ash"],
    "rainy": ["thunderstorm", "drizzle", "rain", "snow"],
    "windy": ["tornado", "squall", "wind"],
    "sunny": ["clear"],
}


def get_weather_conditions() -> Dict[str, str]:
    """
    Get fitted conditions for a pre-trained model.
    """
    weather_conditions = defaultdict(str)

    for target_condition, conditions in CONDITIONS.items():
        for condition in conditions:
            weather_conditions[condition] = target_condition

    return weather_conditions


@dataclass
class WeatherApi:
    api_key: str = os.environ["WEATHER_API_KEY"]
    cities: List[str] = field(init=False, repr=False)
    conditions: Dict[str, str] = field(init=False, default_factory=get_weather_conditions)

    def __post_init__(self) -> None:
        self.cities = self.get_cities()

    def get_cities(self) -> List[str]:
        """
        Read all the city information from json file.
        """
        with open("./config/city_list.json", "r") as file:
            json_files = json.load(file)
            cities = []

            for ob in json_files:
                cities.append(ob["name"])

        return cities

    def get_current_weather(self, city: str = "New York") -> str:
        """
        Get current weather via openweathermap api.
        """
        endpoint = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        url = endpoint.format(key=self.api_key)
        res = requests.get(url)
        data: Dict[str, List[str, str]] = json.loads(res.text)

        return self.conditions[data["weather"][0]["main"].lower()]
