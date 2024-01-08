from time import sleep

import pytest

from rick.base import ShallowContainer
from rick.resource.redis import RedisCache


@pytest.fixture
def redis_cfg():
    return {
        "host": "localhost",
        "port": 63790,
        "password": "myRedisPassword",
        "db": 0,
        "ssl": False,
    }


@pytest.fixture
def redis_client(redis_cfg):
    return RedisCache(**redis_cfg)


class TestRedisCache:

    def test_get_set_remove(self, redis_cfg, redis_client):
        key = "shallow:cfg"
        obj = ShallowContainer(redis_cfg)
        assert redis_client.has(key) is False
        redis_client.set(key, obj)
        assert redis_client.has(key) is True

        record = redis_client.get(key)
        assert record is not None
        assert isinstance(record, ShallowContainer)
        assert list(record.asdict().keys()) == list(redis_cfg.keys())

        assert redis_client.remove(key) == 1
        assert redis_client.has(key) is False
        assert redis_client.remove(key) == 0
        assert redis_client.has(key) is False

    def test_ttl(self,redis_cfg, redis_client):
        key = "shallow:cfg"
        obj = ShallowContainer(redis_cfg)
        assert redis_client.has(key) is False
        redis_client.set(key, obj, ttl=1)
        assert redis_client.has(key) is True
        sleep(2)
        assert redis_client.has(key) is False

    def test_purge(self,redis_cfg, redis_client):
        key = "shallow:cfg"
        obj = ShallowContainer(redis_cfg)
        assert redis_client.has(key) is False
        redis_client.set(key, obj)
        assert redis_client.has(key) is True
        redis_client.purge()
        assert redis_client.has(key) is False

