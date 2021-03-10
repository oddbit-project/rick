import collections
import threading
from typing import Union


class CacheInterface:

    def get(self, key):
        pass

    def set(self, key, value, ttl=None):
        pass

    def has(self, key):
        pass

    def remove(self, key):
        pass

    def purge(self):
        pass

