from typing import List


def get_attribute_names(object) -> List:
    if fieldmap := getattr(object, "_fieldmap", None):
        return list(fieldmap.keys())
    result = []
    for item in dir(object):
        if not item.startswith("_"):
            v = getattr(object, item, None)
            if not callable(v):
                result.append(item)
    return result


def is_object(param):
    if not param:
        return False
    if isinstance(param, object):
        t = str(getattr(param, "__class__"))
        t = t.split("'")[1::2]
        return t[0] not in ["type", "str"]
    return False
