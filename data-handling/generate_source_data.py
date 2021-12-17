import random
from collections import defaultdict

import click
import pandas as pd

from utils import read_params

WEATHER = ["cloudy", "sunny", "rainy", "windy"]
SEASON = ["spring", "summer", "fall", "winter"]


def calculate_estimate_deliver_time(distance: float, current_time: int, weather: str, season: str, traffic: int) -> int:
    """
    Calculate estimate time from restaurant's location to user's location.
    This is random estimate time so it does not correct at all.
    Returns estimate time in minutes.
    """
    estimate_time = 0
    estimate_time += distance * 0.15
    estimate_time *= traffic * 0.01
    if 60 * 11.5 <= current_time <= 60 * 13 or 60 * 17.5 <= current_time <= 60 * 19.5:
        estimate_time *= 1.05
    if weather in ("cloudy", "rainy"):
        estimate_time *= 1.05
    elif weather in ("windy"):
        estimate_time *= 1.005
    if season in ("summer", "winter"):
        estimate_time *= 1.005

    return int(estimate_time // 1 * 60) + int(round(estimate_time % 1, 2) * 60)


@click.command("generate")
@click.option("--amount", default=1000, help="Choose data amount that you are going to generate.")
def main(amount):
    delivery_time = defaultdict(list)

    for _ in range(amount):
        distance = random.randint(1, 1000) / 100
        current_time = random.randint(0, 24 * 60)
        weather = WEATHER[random.randint(0, 3)]
        season = SEASON[random.randint(0, 3)]
        traffic = random.randint(1, 100)
        estimate_deliver_time = calculate_estimate_deliver_time(distance, current_time, weather, season, traffic)

        delivery_time["distance"].append(distance)
        delivery_time["current_time"].append(current_time)
        delivery_time["weather"].append(weather)
        delivery_time["season"].append(season)
        delivery_time["traffic"].append(traffic)
        delivery_time["estimate_deliver_time"].append(estimate_deliver_time)

    config = read_params()
    source_path = config["data"]["source"]

    et_pd = pd.DataFrame(delivery_time)

    et_pd.to_csv(source_path, sep=",", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
