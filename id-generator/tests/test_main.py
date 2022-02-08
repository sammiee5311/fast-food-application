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


def test_generate_id():
    response = client.get("/id-generator/")
    assert response.status_code == status.HTTP_200_OK
    assert "success" in response.json()["message"]


def test_404_page():
    response = client.get("/404/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_id_404_page():
    response = client.get("/id/404/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
