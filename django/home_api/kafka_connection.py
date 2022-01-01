import json
import socket
from typing import Any, Dict, Union

import kafka
from kafka import KafkaProducer

KAFKA_ERRORS = (kafka.errors.NoBrokersAvailable, kafka.errors.UnrecognizedBrokerVersion)

IP_ADDRESS = socket.gethostbyname(socket.gethostname())

JsonObject = Dict[str, Dict[str, Any]]


class TemporaryData:
    def __init__(self):
        self.time_series_database = None

    def send(self, topic: str, order_data: JsonObject):
        """save data in time series database?"""
        print(f"Fail kafak connection : to - {topic} data - {order_data}")


def json_serializer(data) -> JsonObject:
    return json.dumps(data).encode("utf-8")


def conntect_kafka() -> Union[KafkaProducer, TemporaryData]:
    try:
        producer = KafkaProducer(
            security_protocol="PLAINTEXT",
            bootstrap_servers=[f"{IP_ADDRESS}:9092"],
            value_serializer=json_serializer,
            retries=10,
            retry_backoff_ms=1000,
        )

    except KAFKA_ERRORS:
        producer = TemporaryData()

    return producer
