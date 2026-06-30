import threading
import time

import pytest

from rick.base import Di


class Dummy:
    def __init__(self, di):
        pass


class Dummy2:
    def __init__(self, di):
        pass


class TestDi:
    item_mask = "item_{}"

    def test_add(self):
        di = Di()
        # test simple add with a dummy item
        for i in range(0, 10):
            di.add(self.item_mask.format(i), Dummy)

        assert len(di.keys()) == 10
        # check stored items
        for i in range(0, 10):
            item = di.get(self.item_mask.format(i))
            assert isinstance(item, Dummy) is True

        # test adding a duplicate name
        with pytest.raises(RuntimeError):
            di.add(self.item_mask.format(0), Dummy)

        # test replacing a duplicate name
        di.add(self.item_mask.format(0), Dummy2, True)
        item = di.get(self.item_mask.format(0))
        assert isinstance(item, Dummy2) is True

    def test_get(self):
        di = Di()
        # Test get() internal unrapping
        di.add("item1", Dummy)
        di.add("item2", Dummy2)
        assert isinstance(di.get("item1"), Dummy) is True
        assert isinstance(di.get("item2"), Dummy2) is True
        # test exception raise on unknown item
        with pytest.raises(RuntimeError):
            di.get("non-existing-item")

        # test get() with custom factory
        def init_dummy(di):
            return Dummy(di)

        di.add("custom_factory", init_dummy)
        item = di.get("custom_factory")
        assert isinstance(item, Dummy) is True

        # test get() with pre-instantiated object
        obj = Dummy(di)
        di.add("pre-instantiated", obj)
        item = di.get("pre-instantiated")
        assert isinstance(item, Dummy) is True
        assert item.__hash__() == obj.__hash__()

    def test_register_override(self):
        di = Di()

        # test register decorator with a simple custom factory
        @di.register("dep-to-be-overridden")
        def init_dummy(di):
            return Dummy(di)

        item = di.get("dep-to-be-overridden")
        assert isinstance(item, Dummy) is True

        # test override decorator
        @di.override("dep-to-be-overridden")
        def init_dummy2(di):
            return Dummy2(di)

        item = di.get("dep-to-be-overridden")
        assert isinstance(item, Dummy2) is True

    def test_scope(self):
        di = Di()

        # register global dependencies, one of them to be shadowed by a scoped di
        di.add("global-item", Dummy)
        di.add("global-item-will-be-shadowed", Dummy2)

        # create a scoped di called local-di
        local_di = di.scoped("local-di")
        # add a local dependency that will shadow global one
        local_di.add("global-item-will-be-shadowed", Dummy)

        # test get() global via local instance
        assert isinstance(local_di.get("global-item"), Dummy) is True
        # test get() local dependency shadows global one
        assert isinstance(local_di.get("global-item-will-be-shadowed"), Dummy) is True
        # test shadowed global dependency remains unchanged
        assert isinstance(di.get("global-item-will-be-shadowed"), Dummy2) is True

    def test_reentrant_factory(self):
        # a factory may resolve other dependencies via the di passed to it
        di = Di()
        di.add("dep", lambda d: "DEP")
        di.add("svc", lambda d: "svc+" + d.get("dep"))
        assert di.get("svc") == "svc+DEP"
        # memoized: factory result replaces the stored item
        assert di.get("svc") == "svc+DEP"

    def test_concurrent_factory_single_instance(self):
        # a factory dependency resolved concurrently must be built exactly once
        # and hand the same object to every caller
        di = Di()
        calls = []
        calls_lock = threading.Lock()

        def factory(_di):
            time.sleep(0.05)  # widen the concurrency window
            obj = Dummy(_di)
            with calls_lock:
                calls.append(obj)
            return obj

        di.add("svc", factory)
        results = []
        errors = []

        def worker():
            try:
                results.append(di.get("svc"))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(calls) == 1
        assert all(r is calls[0] for r in results)
