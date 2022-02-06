import os
import uuid

import redis

from config.env import load_env

load_env()

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_QUEUE = "UUID"


class UUIDRedis:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def generate_ids(self) -> None:
        """generate ids in redis once a week"""
        for _ in range(1, 1000):
            _uuid = uuid.uuid4().hex

            while self.client.exists(_uuid):
                _uuid = uuid.uuid4().hex

            self.client.lpush(REDIS_QUEUE, _uuid)

    def get_uuid(self) -> str:
        """get uuid from queue which is already generated"""
        try:
            _uuid: bytes = self.client.rpop(REDIS_QUEUE)
        except AttributeError:
            self.generate_ids()

        return _uuid.decode("utf-8")


if __name__ == "__main__":
    _redis = UUIDRedis()
    _redis.generate_ids()
    _redis.get_uuid()
