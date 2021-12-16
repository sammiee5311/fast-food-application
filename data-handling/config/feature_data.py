from enum import Enum
from typing import Any, Dict, Type

from pydantic import BaseModel, Field

from .errors import FeatureDataError


class Weather(str, Enum):
    CLOUDY = "cloudy"
    SUNNY = "sunny"
    RAINNY = "rainny"
    WINDY = "windy"

    @classmethod
    def _missing_(cls, value: str) -> Any:
        values = list(map(lambda x: x.lower(), Weather._member_names_))
        raise FeatureDataError(f"{value!r} is not in {values}")


class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"

    @classmethod
    def _missing_(cls, value: str) -> Any:
        values = list(map(lambda x: x.lower(), Season._member_names_))
        raise FeatureDataError(f"{value!r} is not in {values}")


class Features(BaseModel):
    distance: float = Field(ge=0, le=10, description="distance from restaurant's location to user's location (km)")
    current_time: int = Field(ge=0, le=60 * 24, description="current time which is represented by minutes")
    weather: Weather = Field(description="current weather")
    traffic: int = Field(ge=1, le=100, description="current traffic ratio")
    season: Season = Field(description="current season")

    class Config:
        schema_extra = {
            "example": [
                {
                    "distance": 3.5,
                    "current_time": 245,
                    "weather": Weather("sunny"),
                    "traffic": 34,
                    "season": Season("summer"),
                }
            ]
        }

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type["Features"]) -> None:
            for prop in schema.get("properties", {}).values():
                prop.pop("title", None)
