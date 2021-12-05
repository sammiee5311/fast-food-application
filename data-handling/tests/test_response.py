from typing import List

from utils import get_schema


def get_data() -> List[str]:
    feature_data = "1,2,3,4,5,6,7,8,9,10,11"
    data = list(map(lambda feature: feature.strip(), feature_data.split(",")))

    return data


def test_predict_value(app, client):
    data = get_data()
    payload = {key: val for key, val in zip(list(get_schema().keys()), data)}

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json


def test_predict_error(app, client):
    data = get_data()
    payload = {key: val for key, val in zip(list(get_schema().keys())[:-1], data)}

    response = client.post("/predict", json=payload)

    assert "error" in response.json
