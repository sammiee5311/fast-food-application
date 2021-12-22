import time

import pytest
from config.helper import (
    DistanceError,
    get_current_time,
    get_distance,
    get_season,
    get_traffic,
    get_weather,
    some_machine_leanring_function,
)

json_object1 = {
    "id": 1,
    "username": "test",
    "user_zipcode": "10014",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "restaurant_zipcode": "10009",
    "estimated_delivery_time": None,
}
json_object2 = {
    "id": 1,
    "username": "test",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "restaurant_zipcode": "10009",
    "estimated_delivery_time": None,
}
json_object3 = {
    "id": 1,
    "username": "test",
    "user_zipcode": "10014",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "estimated_delivery_time": None,
}
json_object4 = {
    "id": 1,
    "username": "test",
    "user_zipcode": "10014",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_zipcode": "123124",
    "restaurant_name": "domino's pizza",
    "estimated_delivery_time": None,
}

# @pytest.mark.parametrize(
#     "input, expected", [
#         (json_object1, 0.0)
#     ]
# )
# def test_predict_success(input, expected):
#     distance = get_distance(input)
#     current_time = get_current_time(time.localtime())
#     weather = get_weather()
#     traffic = get_traffic()
#     season = get_season()

#     estimate_time = some_machine_leanring_function(distance, current_time, weather, traffic, season)
#     assert estimate_time * 0 == expected


@pytest.mark.parametrize(
    "input, expected", [(json_object2, DistanceError), (json_object3, DistanceError), (json_object4, DistanceError)]
)
def test_predict_fail(input, expected):
    with pytest.raises(expected):
        distance = get_distance(input)
        current_time = get_current_time(time.localtime())
        weather = get_weather()
        traffic = get_traffic()
        season = get_season()

        some_machine_leanring_function(distance, current_time, weather, traffic, season)
