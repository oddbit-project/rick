import pytest

from rick.resource.redis import CryptRedisCache
from tests.resource.redis.test_redis import TestRedisCache


@pytest.fixture
def redis_cfg():
    return {
        "host": "localhost",
        "port": 63790,
        "password": "myRedisPassword",
        "db": 0,
        "ssl": False,
        "key": "86c5ceb27e1bf441130299c0209e5f35b88089f62c06b2b09d65772274f12057"
    }


@pytest.fixture
def redis_client(redis_cfg):
    return CryptRedisCache(**redis_cfg)


class TestCryptRedisCache(TestRedisCache):

    def test_crypt(self, redis_client):
        key = "test:crypt"
        value = "the quick brown fox jumps over the lazy dog"
        redis_client.set(key, value)