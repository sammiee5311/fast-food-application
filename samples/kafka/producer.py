import json
from time import sleep

from kafka import KafkaProducer

from data import get_registered_user


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def get_partition(*args):
    return 0


if __name__ == "__main__":
    cnt = 0
    producer = KafkaProducer(
        security_protocol="PLAINTEXT",
        bootstrap_servers=["localhost:9092"],
        value_serializer=json_serializer,
    )

    while cnt < 15:
        registered_user = get_registered_user()
        print(registered_user)
        producer.send("registered-user", registered_user)
        cnt += 1
        sleep(3)
