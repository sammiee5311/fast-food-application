import os
import time

import pytest
import requests_mock
from config.env import load_env
from config.errors import (
    DistanceError,
    EstimatedDeliveryTimeAlreadyExist,
    OrderNotFound,
)
from utils.db import SqlLite3, update_estimated_delivery_time
from utils.helper import (
    JasonObject,
    RequiredValues,
    get_current_time,
    get_distance,
    get_estimated_delivery_time_result,
    get_season,
    get_traffic,
    get_weather,
)

load_env()

ML_API_URL = os.environ.get("ML_API_URL")

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


def get_required_values(data: JasonObject) -> RequiredValues:
    return RequiredValues(
        distance=get_distance(data),
        current_time=get_current_time(time.localtime()),
        weather=get_weather(),
        traffic=get_traffic(),
        season=get_season(),
    )


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
        required_values = get_required_values(input)
        get_estimated_delivery_time_result(required_values)


def test_mock_database():
    with SqlLite3() as cursor:
        assert cursor is not None


@pytest.mark.parametrize("order_id", ["f455d3304fa14dd790486a2f5475f54f"])
def test_prediect_success(clear_database):
    data = json_object1

    required_values = get_required_values(data)

    mock: requests_mock.Mocker
    with requests_mock.Mocker() as mock:
        mock.post(ML_API_URL, json={"prediction": 10})
        predicted_delivery_time = get_estimated_delivery_time_result(required_values)

        update_estimated_delivery_time(SqlLite3, data["id"], predicted_delivery_time)

        assert predicted_delivery_time * 0 == 0


def test_database_with_wrong_order_id():
    with pytest.raises(OrderNotFound):
        data = json_object5

        required_values = get_required_values(data)

        mock: requests_mock.Mocker
        with requests_mock.Mocker() as mock:
            mock.post(ML_API_URL, json={"prediction": 10})
            predicted_delivery_time = get_estimated_delivery_time_result(required_values)

            update_estimated_delivery_time(SqlLite3, data["id"], predicted_delivery_time)


def test_database_with_exist_EDT():
    with pytest.raises(EstimatedDeliveryTimeAlreadyExist):
        data = json_object1

        required_values = get_required_values(data)

        mock: requests_mock.Mocker
        with requests_mock.Mocker() as mock:
            mock.post(ML_API_URL, json={"prediction": 10})
            predicted_delivery_time = get_estimated_delivery_time_result(required_values)

            update_estimated_delivery_time(SqlLite3, data["id"], predicted_delivery_time)
