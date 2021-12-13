import os
import socket
from subprocess import CalledProcessError, check_call
from typing import List

import backoff
import kafka
from kafka import KafkaProducer

NORMAL_FILES = ["producer.py"]
FAUST_FILES = ["start.py", "worker"]
KAFKA_ERRORS = (kafka.errors.NoBrokersAvailable, kafka.errors.UnrecognizedBrokerVersion)
IP_ADDRESS = socket.gethostbyname(socket.gethostname())


def backoff_error(e):
    print(f"An error occured : {e}")


@backoff.on_exception(
    backoff.expo,
    KAFKA_ERRORS,
    max_tries=12,
    giveup=backoff_error,
)
def wait_until_kafka_up():
    KafkaProducer(
        security_protocol="PLAINTEXT",
        bootstrap_servers=[f"{IP_ADDRESS}:9092"],
        retries=10,
        retry_backoff_ms=1000,
    )


def excute_sample(path: str, files: List[str]) -> None:
    file = " ".join(files)
    try:
        check_call(f"python {file}", cwd=path, shell=True)
    except CalledProcessError as e:
        print(e)


def check_env(path: str) -> bool:
    env_file = f"{path}/.env"
    with open(env_file, "r") as f:
        for line in f:
            _, value = line.split("=")
            if not value:
                return False

    return True


def main() -> None:
    samples_dir_path = os.path.abspath("./samples")

    for path, _, files in os.walk(samples_dir_path):
        if ".env" in files:
            if check_env(path):
                excute_sample(path, NORMAL_FILES)
        elif "producer.py" in files:
            excute_sample(path, NORMAL_FILES)
        elif "start.py" in files:
            excute_sample(path, FAUST_FILES)


if __name__ == "__main__":
    try:
        wait_until_kafka_up()
        main()
    except KAFKA_ERRORS:
        print("Kafka is not available. (End of sample tests)")
