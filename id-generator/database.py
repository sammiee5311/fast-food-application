import uuid
from typing import List

UUID_HEX = str
UuidQueue = List[UUID_HEX]
uuid_queue: UuidQueue = []

# TODO: Need to use redis instead of txt file.


def generate_ids_in_redis() -> None:
    """generate ids in redis once a week"""
    with open("./uuids.txt", "w") as file:
        for _ in range(1000):
            _uuid = uuid.uuid4()
            file.writelines(f"{_uuid.hex}\n")


def load_uuids_from_redis() -> UuidQueue:
    """load uuids from redis"""
    with open("./uuids.txt", "r") as files:
        uuids = files.readlines()
        uuids = [uuid.strip() for uuid in uuids]

    return uuids


def get_uuid() -> str:
    global uuid_queue
    """get uuid from queue which is already generated"""
    if not uuid_queue:
        uuid_queue = load_uuids_from_redis()

    uuid = uuid_queue.pop()
    return uuid


if __name__ == "__main__":
    generate_ids_in_redis()
    print(get_uuid())
