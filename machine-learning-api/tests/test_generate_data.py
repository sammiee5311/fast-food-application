import random

from generate_source_data import calculate_estimate_deliver_time

WEATHER = ["cloudy", "sunny", "rainy", "windy"]
SEASON = ["spring", "summer", "fall", "winter"]


def test_generate_source_data():
    distance = random.randint(1, 1000) / 100
    current_time = random.randint(0, 24 * 60)
    weather = WEATHER[random.randint(0, 3)]
    season = SEASON[random.randint(0, 3)]
    traffic = random.randint(1, 100)

    estimate_deliver_time = calculate_estimate_deliver_time(distance, current_time, weather, season, traffic)

    assert 0 <= estimate_deliver_time <= 100
