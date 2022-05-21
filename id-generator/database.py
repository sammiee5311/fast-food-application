import os
import uuid

import fakeredis
import redis

from config.env import load_env
from utils.log import logger

load_env()

TESTING = os.environ.get("TESTING", False)
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_QUEUE = "UUID"
GEN_UUIDS = 100


class UUIDRedis:
    def __init__(self):
        self.client = (
            redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
            if not TESTING
            else fakeredis.FakeRedis()
        )

    def generate_ids(self) -> None:
        """generate ids in redis once a week"""
        logger.info("Generating uuids.")
        for _ in range(GEN_UUIDS):
            _uuid = uuid.uuid4().hex

            while self.client.exists(_uuid):
                _uuid = uuid.uuid4().hex

            self.client.lpush(REDIS_QUEUE, _uuid)

    def get_uuid(self) -> str:
        """get uuid from queue which is already generated"""
        _uuid: bytes = self.client.rpop(REDIS_QUEUE)
        logger.info("Getting an uuid from cache.")
        if not _uuid:
            self.generate_ids()
            _uuid: bytes = self.client.rpop(REDIS_QUEUE)

        return _uuid.decode("utf-8")


if __name__ == "__main__":
    _redis = UUIDRedis()
    _redis.generate_ids()
    _redis.get_uuid()
