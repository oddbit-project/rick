import threading
import time

import pytest

from rick.base import Di, MapLoader


class MapDummy:
    def __init__(self, di):
        self.di = di


class MapSlow:
    def __init__(self, di):
        # slow build to widen the cross-thread resolution window
        time.sleep(0.05)


class MapCyclic:
    def __init__(self, di):
        # re-enter the loader for the same name -> circular dependency
        di.get("loader").get("cyclic")


def test_get_and_cache():
    loader = MapLoader(Di())
    loader.add("dummy", "tests.base.test_maploader.MapDummy")
    obj = loader.get("dummy")
    assert isinstance(obj, MapDummy)
    # subsequent gets return the cached instance
    assert loader.get("dummy") is obj


def test_unknown_name():
    loader = MapLoader(Di())
    with pytest.raises(ValueError):
        loader.get("missing")


def test_circular_dependency():
    di = Di()
    loader = MapLoader(di)
    di.add("loader", loader)
    loader.add("cyclic", "tests.base.test_maploader.MapCyclic")
    with pytest.raises(RuntimeError):
        loader.get("cyclic")


def test_concurrent_same_name():
    # resolving the same name from several threads must not raise a false
    # "circular dependency" (the re-entrancy stack is thread-local)
    loader = MapLoader(Di())
    loader.add("slow", "tests.base.test_maploader.MapSlow")
    errors = []
    results = []

    def worker():
        try:
            results.append(loader.get("slow"))
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    assert len(results) == 8
