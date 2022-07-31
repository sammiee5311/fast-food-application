import json
import socket
from typing import Any, Dict, Union

import kafka
from kafka import KafkaProducer

KAFKA_ERRORS = (kafka.errors.NoBrokersAvailable, kafka.errors.UnrecognizedBrokerVersion)

IP_ADDRESS = "kafka"

JsonObject = Dict[str, Dict[str, Any]]


class TemporaryData:
    def __init__(self):
        from api.redis_data.config import Redis

        self.redis = Redis()

    def send(self, topic: str, order_data: JsonObject):
        """save data in time series database?"""
        print(f"Fail kafak connection : to - {topic} data - {order_data}")
        self.redis.add(order_data)

    def is_empty(self) -> bool:
        return self.redis.is_empty()


def json_serializer(data) -> JsonObject:
    return json.dumps(data).encode("utf-8")


def check_local_data_and_send_to_kafka(producer: KafkaProducer) -> None:
    order_data = TemporaryData().redis.get()

    while order_data:
        producer.send("fast-food-order", order_data)


def conntect_kafka() -> Union[KafkaProducer, TemporaryData]:
    try:
        producer = KafkaProducer(
            security_protocol="PLAINTEXT",
            bootstrap_servers=[f"{IP_ADDRESS}:29092"],
            value_serializer=json_serializer,
            retries=10,
            retry_backoff_ms=1000,
        )

        check_local_data_and_send_to_kafka(producer)

    except KAFKA_ERRORS:
        producer = TemporaryData()

    return producer
