import json
import sys
from typing import Any, Dict, Optional

import fakeredis
import redis
from core.settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

REDIS_QUEUE = "KAFKA_LOCAL"
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

JsonObject = Dict[str, Dict[str, Any]]


class Redis:
    def __init__(self, client: redis.Redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)):
        self.client = client if not TESTING else fakeredis.FakeRedis()

    def add(self, order_data: JsonObject) -> None:
        self.client.lpush(REDIS_QUEUE, json.dumps(order_data))

    def get(self) -> Optional[JsonObject]:
        order_data = self.client.rpop(REDIS_QUEUE)
        return json.loads(order_data) if order_data else None
