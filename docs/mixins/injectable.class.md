# Mixin rick.mixin.**Injectable**

Mixin that provides dependency injection integration. Classes that extend `Injectable` receive a
[Di](../base/index.md#di-dependency-injection) container on construction.

**Location:** `rick.mixin.Injectable`

## Constructor

### Injectable.**__init__(di: Di)**

Store the `Di` container instance.

**Parameters:**

- `di` (Di) - Dependency injection container

## Methods

### Injectable.**set_di(di: Di)**

Replace the internal `Di` reference.

### Injectable.**get_di() -> Di**

Retrieve the internal `Di` container.

## Usage

```python
from rick.mixin import Injectable
from rick.base import Di


class UserService(Injectable):
    def __init__(self, di: Di):
        super().__init__(di)

    def get_user(self, user_id):
        db = self.get_di().get('db')
        return db.find_user(user_id)


# Register and use
di = Di()
di.add('db', my_database)
di.add('user_service', UserService)

service = di.get('user_service')
user = service.get_user(123)
```

`Injectable` is commonly used as a base class for services that need access to the DI container
and are loaded via [MapLoader](../base/index.md#maploader).

## Related Topics

- [Di](../base/index.md#di-dependency-injection) - Dependency injection container
- [Runnable](runnable.class.md) - Runnable interface mixin
- [Translator](translator.class.md) - Translation mixin
