import pytest
from main import predict

json_obect1 = {
    "username": "test",
    "user_zipcode": "10014",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "restaurant_zipcode": "10009",
    "estimated_delivery_time": None,
}
json_obect2 = {
    "username": "test",
    "restaurant_zipcode": "10009",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "estimated_delivery_time": None,
}
json_obect3 = {
    "username": "test",
    "user_zipcode": "10014",
    "created_on_str": "2021-12-19 08:06",
    "menus": ["pizza"],
    "restaurant_name": "domino's pizza",
    "estimated_delivery_time": None,
}


@pytest.mark.parametrize("input, expected", [(json_obect1, (-1.0, 53)), (json_obect2, (0, 0)), (json_obect3, (0, 0))])
def test_predict(input, expected):
    data = input
    result = predict(data)
    assert result[0] == expected[0]
