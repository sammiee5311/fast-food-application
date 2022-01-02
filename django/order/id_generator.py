from uuid import UUID, uuid4

import requests
from requests import Response

HOST = "localhost"
PORT = 8008


class APIConnectionError(Exception):
    def __init__(self, message="id generator server cannot be connected"):
        self.message = message
        super().__init__(self.message)


def connect_to_server() -> Response:
    try:
        response = requests.get(f"http://{HOST}:{PORT}/id")

        if response.status_code != 201:
            raise APIConnectionError()

        return response

    except Exception:  # TODO: implement
        raise APIConnectionError()


def get_uuid() -> UUID:
    try:
        response = connect_to_server()

        payload = response.json()

        uuid_payload = payload["uuid"]
        _uuid = UUID(uuid_payload)

        return _uuid
    except Exception:  # TODO: need to implement
        return uuid4()
