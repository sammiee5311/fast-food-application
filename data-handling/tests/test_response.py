from gcli import FEATURES


def test_predict_value(app, client):
    feature_data = "1,2,3,4,5,6,7,8,9,10,11"
    _data = list(map(lambda feature: feature.strip(), feature_data.split(",")))
    payload = {key: val for key, val in zip(FEATURES, _data)}

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json
