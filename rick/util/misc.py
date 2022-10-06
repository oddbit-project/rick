def optional(name, src: dict, default=None):
    if name in src.keys():
        return src[name]
    return default
