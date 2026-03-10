from typing import List


def get_attribute_names(object) -> List:
    fieldmap = getattr(object, "_fieldmap", None)
    if fieldmap:
        return list(fieldmap.keys())
    result = []
    for item in dir(object):
        if not item.startswith("_"):
            v = getattr(object, item, None)
            if not callable(v):
                result.append(item)
    return result


def is_object(param):
    if param is None:
        return False
    if isinstance(param, (str, int, float, bool, bytes, list, tuple, dict, set)):
        return False
    if isinstance(param, type):
        return False
    return hasattr(param, "__dict__")


def full_name(obj):
    return obj.__class__.__module__ + "." + obj.__class__.__name__
