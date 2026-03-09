# Utilities

The `rick.util` package provides small helper functions organized by topic.

## cast

Type casting functions that return `None` on failure instead of raising exceptions.

**Location:** `rick.util.cast`

```python
from rick.util.cast import cast_str, cast_int, cast_float
```

| Function              | Returns        | Description                          |
|-----------------------|----------------|--------------------------------------|
| `cast_str(value)`     | str or None    | Convert to string; `None` on failure |
| `cast_int(value)`     | int or None    | Convert to int; `None` on failure    |
| `cast_float(value)`   | float or None  | Convert to float; `None` on failure  |

```python
cast_int("42")    # 42
cast_int("abc")   # None
cast_float("3.14") # 3.14
cast_str(123)     # "123"
```

## datetime

Date/time utilities.

**Location:** `rick.util.datetime`

```python
from rick.util.datetime import iso8601_now
```

### iso8601_now() -> str

Return the current date and time as an ISO 8601 string with timezone info.

```python
iso8601_now()  # '2025-11-06T10:30:45.123456+00:00'
```

## loader

Dynamic class loading.

**Location:** `rick.util.loader`

```python
from rick.util.loader import load_class
```

### load_class(path: str, raise_exception: bool = False) -> class or None

Load a class by its dotted module path.

```python
cls = load_class('rick.resource.redis.RedisCache')
cache = cls(host='localhost')

# Raises ModuleNotFoundError if not found
cls = load_class('nonexistent.Module', raise_exception=True)
```

**Parameters:**

- `path` (str) - Dotted path (e.g. `'package.module.ClassName'`)
- `raise_exception` (bool) - If `True`, raise `ModuleNotFoundError` on failure instead of returning `None`

## misc

Miscellaneous helpers.

**Location:** `rick.util.misc`

```python
from rick.util.misc import list_duplicates
```

### list_duplicates(origin: list) -> list

Return a list of duplicate items found in `origin`.

```python
list_duplicates([1, 2, 3, 2, 4, 3])  # [2, 3]
list_duplicates([1, 2, 3])            # []
```

## object

Object introspection utilities.

**Location:** `rick.util.object`

```python
from rick.util.object import get_attribute_names, is_object, full_name
```

### get_attribute_names(obj) -> list

Get a list of public, non-callable attribute names from an object. If the object has a `_fieldmap`
attribute, its keys are used instead.

```python
class User:
    name = "John"
    age = 30
    def greet(self):
        pass

get_attribute_names(User())  # ['age', 'name']
```

### is_object(param) -> bool

Check if `param` is an object instance (not a type, str, or falsy value).

### full_name(obj) -> str

Return the fully qualified class name of an object.

```python
from rick.base import Di
full_name(Di())  # 'rick.base.di.Di'
```

## string

String case conversion utilities.

**Location:** `rick.util.string`

```python
from rick.util.string import snake_to_camel, snake_to_pascal
```

### snake_to_camel(src: str) -> str

Convert `snake_case` to `camelCase`.

```python
snake_to_camel('user_first_name')  # 'userFirstName'
```

### snake_to_pascal(src: str) -> str

Convert `snake_case` to `PascalCase`.

```python
snake_to_pascal('user_first_name')  # 'UserFirstName'
```

## Related Topics

- [Base Classes](../base/index.md) - DI, containers, registries
- [Filters](../filters/index.md) - Filters use cast functions internally
