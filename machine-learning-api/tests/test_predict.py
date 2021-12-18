import pytest
from main import predict

json_obect1 = {}
json_obect2 = {}
json_obect3 = {}


@pytest.mark.parametrize("input, expected", [(json_obect1, 1), (json_obect2, 0), (json_obect3, 0)])
def test_predict(input, expected):
    data = None
    result = predict(data)
    assert result == 0
