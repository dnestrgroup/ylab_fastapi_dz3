import json
from typing import Any, Dict

import pytest

from app.db.redis.redis import redis_client
from app.tests.conftest import TestClientBase


class TestRedis(TestClientBase):
    @pytest.mark.asyncio
    @pytest.mark.redis
    async def test_redis(self) -> None:
        # data = json.dumps({"test_data": 1})
        # redis_client.setex("2", 10, data.encode())
        # cached_data = redis_client.get("2")
        # if cached_data:
        #     assert cached_data.decode() == data
        # assert cached_data is not None

        temp = redis_client.keys("*")
        print("redis = ", temp)
