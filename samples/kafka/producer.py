import json
import socket
from time import sleep

from data import get_registered_user
from kafka import KafkaProducer


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def get_partition(*args):
    return 0


if __name__ == "__main__":
    cnt = 0
    ip_address = socket.gethostbyname(socket.gethostname())
    producer = KafkaProducer(
        security_protocol="PLAINTEXT",
        bootstrap_servers=[f"{ip_address}:9092"],
        value_serializer=json_serializer,
        retries=10,
        retry_backoff_ms=1000,
    )

    while cnt < 10:
        registered_user = get_registered_user()
        print(registered_user)
        producer.send("registered-user", registered_user)
        cnt += 1
        sleep(2)
