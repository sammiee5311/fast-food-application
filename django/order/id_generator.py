from typing import Dict
from uuid import UUID, uuid4

import requests
from core.tracing import tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from requests import Response

HOST = "id-generator"
PORT = 8008


class APIConnectionError(Exception):
    def __init__(self, message="id generator server cannot be connected"):
        self.message = message
        super().__init__(self.message)


def inject_tracing_if_enable() -> Dict[str, str]:
    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        headers = {"traceparent": carrier["traceparent"]}
    except LookupError:
        headers = {}

    return headers


def connect_to_server() -> Response:
    try:
        headers = inject_tracing_if_enable()
        response = requests.get(f"http://{HOST}:{PORT}/id", headers=headers)

        if response.status_code != 200:
            raise APIConnectionError()

        return response

    except Exception:  # TODO: implement
        raise APIConnectionError()


def get_uuid() -> UUID:
    try:
        with tracer.start_as_current_span("get-uuid") as span:
            response = connect_to_server()

            payload = response.json()

            uuid_payload = payload["uuid"]
            _uuid = UUID(uuid_payload)

            if span.is_recording():
                span.set_attribute("uuid", uuid_payload)

            return _uuid
    except Exception:  # TODO: need to implement
        return uuid4()
