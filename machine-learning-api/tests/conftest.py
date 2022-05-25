import os

import pytest
from app import app as flask_app
from src.get_dataset import read_params


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def config():
    config_path = os.path.join("config", "params.yaml")
    config = read_params(config_path)

    return config
