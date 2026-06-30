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


class MapCounted:
    builds = 0
    _lock = threading.Lock()

    def __init__(self, di):
        # slow build to widen the concurrent cold-start window
        time.sleep(0.05)
        with MapCounted._lock:
            MapCounted.builds += 1

    @classmethod
    def reset(cls):
        with cls._lock:
            cls.builds = 0


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


def test_concurrent_builds_once():
    # concurrent cold-start must construct the object exactly once and every
    # caller must observe the same instance (#2b)
    MapCounted.reset()
    loader = MapLoader(Di())
    loader.add("counted", "tests.base.test_maploader.MapCounted")
    results = []
    barrier = threading.Barrier(8)

    def worker():
        barrier.wait()
        results.append(loader.get("counted"))

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert MapCounted.builds == 1
    assert len(results) == 8
    assert all(r is results[0] for r in results)


def test_clear_loaded_rebuilds():
    # clearing the loaded cache must force a fresh build (no stale memoization)
    MapCounted.reset()
    loader = MapLoader(Di())
    loader.add("counted", "tests.base.test_maploader.MapCounted")
    first = loader.get("counted")
    assert MapCounted.builds == 1
    loader.clear_loaded()
    second = loader.get("counted")
    assert MapCounted.builds == 2
    assert second is not first


def test_remove_clears_loaded():
    # removing a name must drop its cached instance so a re-add rebuilds
    MapCounted.reset()
    loader = MapLoader(Di())
    loader.add("counted", "tests.base.test_maploader.MapCounted")
    first = loader.get("counted")
    loader.remove("counted")
    with pytest.raises(ValueError):
        loader.get("counted")
    loader.add("counted", "tests.base.test_maploader.MapCounted")
    second = loader.get("counted")
    assert MapCounted.builds == 2
    assert second is not first
