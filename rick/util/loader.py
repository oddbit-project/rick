import importlib
from typing import Optional


def load_class(path: str, raise_exception: bool = False) -> Optional[object]:
    """
    Loads a class by string path
    :param path: string path
    :param raise_exception: bool if True, exception is raised if resource is not found
    :return: either a class or None if resource is not found
    """
    try:
        module_path, cls_name = path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, cls_name, None)
        if cls is None:
            if raise_exception:
                raise ModuleNotFoundError(path)

            else:
                return None
        return cls
    except ModuleNotFoundError:
        if not raise_exception:
            return None
        raise
