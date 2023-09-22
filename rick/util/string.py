def snake_to_camel(src: str) -> str:
    if words := src.split("_"):
        return words[0] + "".join(word.title() for word in words[1:])
    return src


def snake_to_pascal(src: str) -> str:
    if words := src.split("_"):
        return "".join(word.title() for word in words)
    return src
