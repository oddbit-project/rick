# Mixin rick.mixin.**Runnable**

Mixin that defines a runnable interface. Classes that extend `Runnable` implement a `run()` method
that receives a [Di](../base/index.md#di-dependency-injection) container.

**Location:** `rick.mixin.Runnable`

## Methods

### Runnable.**run(di: Di)**

Execute the runnable. The default implementation is a no-op; subclasses should override this method.

**Parameters:**

- `di` (Di) - Dependency injection container

## Usage

```python
from rick.mixin import Runnable
from rick.base import Di


class MigrationTask(Runnable):
    def run(self, di: Di):
        db = di.get('db')
        db.execute('ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT TRUE')
        print("Migration complete")


class SeedTask(Runnable):
    def run(self, di: Di):
        db = di.get('db')
        db.execute("INSERT INTO users (name) VALUES ('admin')")
        print("Seeding complete")


# Execute tasks
di = Di()
di.add('db', my_database)

tasks = [MigrationTask(), SeedTask()]
for task in tasks:
    task.run(di)
```

## Related Topics

- [Di](../base/index.md#di-dependency-injection) - Dependency injection container
- [Injectable](injectable.class.md) - DI integration mixin
- [Translator](translator.class.md) - Translation mixin
