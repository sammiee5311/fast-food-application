import os
import socket
from subprocess import CalledProcessError, check_call, run
from typing import List

import backoff
import kafka
from kafka import KafkaProducer

NORMAL_FILES = ["producer.py"]
FAUST_FILES = ["start.py", "worker"]


@backoff.on_exception(
    backoff.expo, (kafka.errors.NoBrokersAvailable, kafka.errors.UnrecognizedBrokerVersion), max_tries=15
)
def wait_until_kafka_up():
    KafkaProducer(bootstrap_servers=f"{socket.gethostbyname(socket.gethostname())}:9092")


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
    wait_until_kafka_up()
    main()
