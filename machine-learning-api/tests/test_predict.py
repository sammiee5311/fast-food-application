import time

import pytest
from config.env import load_env
from config.errors import (
    APIConnectionError,
    DistanceError,
    EstimatedDeliveryTimeAlreadyExist,
    OrderNotFound,
)
from utils.db import SqlLite3, update_estimated_delivery_time
from utils.helper import (
    get_current_time,
    get_distance,
    get_season,
    get_traffic,
    get_weather,
    some_machine_leanring_function,
)

load_env()

json_object1 = {
    "id": "f455d3304fa14dd790486a2f5475f54f",
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
json_object5 = {
    "id": "f455d3304fa14dd790486a2f5475f5f",
    "username": "test",
    "user_zipcode": "10014",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "restaurant_zipcode": "10009",
    "estimated_delivery_time": None,
}


@pytest.mark.parametrize(
    "input, expected",
    [
        (json_object2, DistanceError),
        (json_object3, DistanceError),
        (json_object4, DistanceError),
    ],
)
def test_predict_fail(input, expected):
    with pytest.raises(expected):
        distance = get_distance(input)
        current_time = get_current_time(time.localtime())
        weather = get_weather()
        traffic = get_traffic()
        season = get_season()

        some_machine_leanring_function(distance, current_time, weather, traffic, season)


def test_mock_database():
    with SqlLite3() as cursor:
        assert cursor is not None


@pytest.mark.parametrize("order_id", ["f455d3304fa14dd790486a2f5475f54f"])
def test_prediect_success(clear_database):
    data = json_object1

    distance = get_distance(data)
    current_time = get_current_time(time.localtime())
    weather = get_weather()
    traffic = get_traffic()
    season = get_season()

    predicted_delivery_time = some_machine_leanring_function(distance, current_time, weather, traffic, season)
    update_estimated_delivery_time(SqlLite3, data["id"], predicted_delivery_time)

    assert predicted_delivery_time * 0 == 0


def test_database_with_wrong_order_id():
    with pytest.raises(OrderNotFound):
        data = json_object5

        distance = get_distance(data)
        current_time = get_current_time(time.localtime())
        weather = get_weather()
        traffic = get_traffic()
        season = get_season()

        predicted_delivery_time = some_machine_leanring_function(distance, current_time, weather, traffic, season)

        update_estimated_delivery_time(SqlLite3, data["id"], predicted_delivery_time)


def test_database_with_exist_EDT():
    with pytest.raises(EstimatedDeliveryTimeAlreadyExist):
        data = json_object1

        distance = get_distance(data)
        current_time = get_current_time(time.localtime())
        weather = get_weather()
        traffic = get_traffic()
        season = get_season()

        predicted_delivery_time = some_machine_leanring_function(distance, current_time, weather, traffic, season)

        update_estimated_delivery_time(SqlLite3, data["id"], predicted_delivery_time)
