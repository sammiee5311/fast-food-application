from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "This server is an api for id generator."}


def test_get_id():
    response = client.get("/id/")
    assert response.status_code == status.HTTP_200_OK
    assert "uuid" in response.json()
