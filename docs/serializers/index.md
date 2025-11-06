# Serializers

Rick provides serializers for converting Python objects to and from various data formats. The serializer module offers extended support for complex Python types that standard serializers don't handle natively.

## Overview

Serializers in Rick extend standard serialization libraries with support for:

- **datetime.date** and **datetime.datetime** objects
- **decimal.Decimal** for precise numeric operations
- **uuid.UUID** objects
- **Dataclasses** with nested support
- **Custom Python objects** with `__dict__` attributes
- **Memoryview** and **bytes** objects

## Available Serializers

Rick currently provides two serializers:

- **[JSON Serializer](json.md)** - Extended JSON encoding with support for Python types
- **[MessagePack Serializer](msgpack.md)** - Binary serialization and deserialization with custom type extensions

## Common Use Cases

### API Responses

```python
from rick.serializer.json import ExtendedJsonEncoder
import json

data = {
    'user_id': uuid.uuid4(),
    'created_at': datetime.datetime.now(),
    'balance': decimal.Decimal('123.45')
}

# Serialize for API response
response = json.dumps(data, cls=ExtendedJsonEncoder)
```

### Data Caching

```python
from rick.serializer.msgpack import msgpack

# Serialize for cache storage
cached_data = msgpack.packb(complex_object)

# Deserialize from cache
restored_data = msgpack.unpackb(cached_data)
```

### Configuration with Custom Types

```python
from rick.serializer.json import ExtendedJsonEncoder
import json

config = {
    'api_key': uuid.uuid4(),
    'timeout': decimal.Decimal('30.5'),
    'last_updated': datetime.datetime.now()
}

# Save configuration
with open('config.json', 'w') as f:
    json.dump(config, f, cls=ExtendedJsonEncoder, indent=2)
```

## Type Support

| Type | JSON | MessagePack |
|------|------|-------------|
| datetime.date | ISO string | Binary extension |
| datetime.datetime | ISO string | Binary extension |
| decimal.Decimal | String | String in extension |
| uuid.UUID | String | 16-byte binary |
| Dataclass | Dict | Dict with class info |
| Custom objects | Dict | Dict with reconstruction |
| Memoryview | UTF-8 string | Binary |
| bytes | UTF-8 string | Binary |
