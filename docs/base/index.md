# Base Classes

The `rick.base` module provides foundational building blocks: dependency injection, data containers, registries,
and dynamic class loading.

**Location:** `rick.base`

```python
from rick.base import Di, Container, MutableContainer, ShallowContainer, Registry, ClassRegistry, MapLoader
```

## Di (Dependency Injection)

A service container with singleton semantics and support for factory functions.

**Location:** `rick.base.Di`

### Constructor

```python
Di(di=None)
```

- `di` (Di, optional) - Parent `Di` instance for scoped containers

### Methods

#### Di.**add(name: str, item, replace=False)**

Register a dependency. If `item` is a class, it will be wrapped in a factory that receives the `Di` instance
on first retrieval. If `item` is an object, callable, or lambda, it is stored directly.

```python
di = Di()

# Register an object
di.add('config', {'debug': True})

# Register a class (instantiated lazily with di as argument)
di.add('cache', RedisCache)

# Register a factory
di.add('logger', lambda di: Logger(di.get('config')))
```

**Raises:** `RuntimeError` if name already exists and `replace` is `False`

#### Di.**get(name: str)**

Retrieve a dependency. Results are cached via `lru_cache` — callables and factories are executed once on first
access, and the result replaces the factory in the registry.

```python
config = di.get('config')
```

**Raises:** `RuntimeError` if name is not found (checks parent if scoped)

#### Di.**has(name: str) -> bool**

Check if a dependency name is registered.

#### Di.**keys() -> list**

Return a list of all registered names.

#### Di.**register(name: str)**

Decorator to register a class:

```python
@di.register('service')
class MyService:
    def __init__(self, di):
        pass
```

#### Di.**override(name: str)**

Decorator to replace an existing dependency.

#### Di.**scoped(name: str) -> Di**

Create a child `Di` instance. The child can access parent dependencies via `get()`.

```python
child = di.scoped('request_scope')
child.add('user', current_user)
child.get('config')  # falls through to parent
```

#### Di.**is_scoped() -> bool**

Returns `True` if this instance has a parent.

#### Di.**get_parent() -> Di**

Returns the parent `Di` instance, or `None`.

## Container

Immutable (read-only) container that deep-copies initial data. Changes to the original dict do not affect
the container.

**Location:** `rick.base.Container`

```python
from rick.base import Container

data = {'host': 'localhost', 'port': 5432}
c = Container(data)

print(c['host'])       # 'localhost'
print(c.get('port'))   # 5432
print(c.has('host'))   # True
print(len(c))          # 2
print(c.asdict())      # {'host': 'localhost', 'port': 5432} (deep copy)
```

Nested dicts are automatically wrapped as `Container` on access:

```python
c = Container({'db': {'host': 'localhost'}})
db = c['db']  # Container({'host': 'localhost'})
```

### Methods

| Method              | Returns         | Description                              |
|---------------------|-----------------|------------------------------------------|
| `has(key)`          | bool            | Check if key exists                      |
| `get(key, default)` | Any             | Get value or default                     |
| `asdict()`          | dict            | Return a deep copy of the data           |
| `keys()`            | KeysView        | Return keys                              |
| `values()`          | list            | Return list of values                    |
| `copy()`            | Container       | Return a new Container copy              |

## MutableContainer

Mutable container that supports updates, deletions, and clearing.

**Location:** `rick.base.MutableContainer`

```python
from rick.base import MutableContainer

mc = MutableContainer({'key': 'value'})
mc['new_key'] = 'new_value'
mc.update('key', 'updated')
del mc['new_key']
mc.clear()
```

### Additional Methods

| Method              | Description                    |
|---------------------|--------------------------------|
| `update(key, value)`| Set a key-value pair           |
| `clear()`           | Remove all entries             |
| `remove(key)`       | Remove a specific key          |

Also supports `__setitem__` and `__delitem__`.

## ShallowContainer

Immutable (read-only) container that does **not** copy initial data. If the underlying dict changes,
the container reflects those changes.

**Location:** `rick.base.ShallowContainer`

```python
from rick.base import ShallowContainer

data = {'key': 'value'}
sc = ShallowContainer(data)

data['key'] = 'changed'
print(sc['key'])  # 'changed'
```

Same API as `Container`, but `asdict()` returns the original dict reference.

## Registry

Thread-safe registry for storing object instances. Registered objects must be instances of a
specified prototype class.

**Location:** `rick.base.Registry`

```python
from rick.base import Registry

class Plugin:
    pass

registry = Registry(Plugin)
```

### Registry.**register_cls(name: str, override: bool = False)**

Decorator that instantiates the class and stores the instance:

```python
@registry.register_cls('my_plugin')
class MyPlugin(Plugin):
    pass
```

### Registry.**register_obj(name: str, obj, override: bool = False)**

Register an existing object instance:

```python
registry.register_obj('custom', MyPlugin())
```

### Common Methods

| Method         | Returns | Description                                 |
|----------------|---------|---------------------------------------------|
| `get(name)`    | object  | Retrieve by name (raises `ValueError`)      |
| `has(name)`    | bool    | Check if name is registered                 |
| `names()`      | list    | List registered names                       |
| `remove(name)` | None    | Remove entry by name                        |

## ClassRegistry

Thread-safe registry for storing classes (not instances). Registered classes must be subclasses of
a specified prototype.

**Location:** `rick.base.ClassRegistry`

```python
from rick.base import ClassRegistry

class Handler:
    pass

class_registry = ClassRegistry(Handler)

@class_registry.register('json')
class JsonHandler(Handler):
    pass

# Retrieve the class (not an instance)
handler_cls = class_registry.get('json')
obj = handler_cls()
```

### ClassRegistry.**register(name: str, override: bool = False)**

Decorator that stores the class itself.

### ClassRegistry.**register_cls(name: str, cls, override: bool = False)**

Register a class directly.

## MapLoader

Dynamic class loader that resolves dotted paths to classes and instantiates them with the `Di`
container. Results are cached and circular dependencies are detected.

**Location:** `rick.base.MapLoader`

```python
from rick.base import Di, MapLoader

di = Di()
loader = MapLoader(di, {
    'cache': 'myapp.services.CacheService',
    'mailer': 'myapp.services.MailService',
})

cache = loader.get('cache')   # imports and instantiates CacheService(di)
mailer = loader.get('mailer') # imports and instantiates MailService(di)
```

### Methods

| Method                    | Description                                      |
|---------------------------|--------------------------------------------------|
| `add(name, path)`         | Add a single mapping entry                       |
| `append(map: dict)`       | Add multiple entries from a dict                 |
| `get(name)`               | Load, instantiate, cache, and return the object  |
| `contains(name)`          | Check if name exists in the map                  |
| `remove(name)`            | Remove entry and clear cache                     |
| `clear_loaded()`          | Remove all cached instances                      |
| `register(name, obj)`     | Register a pre-built object directly             |
| `build(cls)`              | Override to customize instantiation              |

## Related Topics

- [Mixins](../mixins/injectable.class.md) - Injectable mixin for DI integration
- [Configuration](../resources/config.md) - Configuration loading utilities
