# MessagePack Serializer

The MessagePack serializer in Rick provides efficient binary serialization with full support for complex Python types.
Unlike the JSON serializer, MessagePack supports bidirectional serialization (encoding and decoding) with type
preservation.

**Location:** `rick.serializer.msgpack`

## Overview

Rick's MessagePack serializer extends the standard `msgpack` library with custom extension types for Python-specific
objects.

## Supported Types

The serializer uses MessagePack extension types to preserve Python object types:

| Type                | Extension Code          | Encoding Method       | Decoding Method            |
|---------------------|-------------------------|-----------------------|----------------------------|
| `datetime.date`     | EXT_TYPE_DATE (1)       | ISO format string     | `fromisoformat()`          |
| `datetime.datetime` | EXT_TYPE_DATETIME (2)   | ISO format string     | `fromisoformat()`          |
| `decimal.Decimal`   | EXT_TYPE_DECIMAL (3)    | String representation | `Decimal()` constructor    |
| `uuid.UUID`         | EXT_TYPE_UUID (4)       | 16-byte binary        | `UUID(bytes=...)`          |
| Dataclasses         | EXT_TYPE_DATACLASS (5)  | Dict with class info  | Dynamic reconstruction     |
| `memoryview`        | EXT_TYPE_MEMORYVIEW (6) | Binary bytes          | `memoryview()` constructor |
| Custom objects      | EXT_TYPE_OBJECT (7)     | Dict with class info  | Dynamic reconstruction     |

## API Functions

### packb()

Serialize a Python object to MessagePack bytes.

```python
from rick.serializer.msgpack import msgpack

data = {'key': 'value', 'number': 42}
packed = msgpack.packb(data)
```

**Parameters:**

- `obj` - Object to serialize
- `**kwargs` - Additional arguments passed to `msgpack.packb()`

**Returns:** Serialized bytes

### unpackb()

Deserialize MessagePack bytes to a Python object.

```python
from rick.serializer import msgpack

packed = b'\x82\xa3key\xa5value\xa6number*'
data = msgpack.unpackb(packed)
```

**Parameters:**

- `packed` - Serialized bytes
- `**kwargs` - Additional arguments passed to `msgpack.unpackb()`

**Returns:** Deserialized Python object

### pack()

Serialize a Python object to a stream.

```python
from rick.serializer import msgpack

with open('data.msgpack', 'wb') as f:
    msgpack.pack({'key': 'value'}, f)
```

**Parameters:**

- `obj` - Object to serialize
- `stream` - File-like object to write to
- `**kwargs` - Additional arguments passed to `msgpack.pack()`

### unpack()

Deserialize a Python object from a stream.

```python
from rick.serializer import msgpack

with open('data.msgpack', 'rb') as f:
    data = msgpack.unpack(f)
```

**Parameters:**

- `stream` - File-like object to read from
- `**kwargs` - Additional arguments passed to `msgpack.unpack()`

**Returns:** Deserialized Python object

## Basic Usage Examples

### Simple Data Types

```python
from rick.serializer import msgpack

# Serialize basic types
data = {
    'string': 'hello',
    'integer': 42,
    'float': 3.14,
    'boolean': True,
    'list': [1, 2, 3],
    'nested': {'a': 1, 'b': 2}
}

packed = msgpack.packb(data)
restored = msgpack.unpackb(packed)

assert data == restored
```

### DateTime Objects

```python
from datetime import datetime, date
from rick.serializer import msgpack

data = {
    'created_at': datetime.now(),
    'birth_date': date(1990, 5, 15),
    'updated_at': datetime(2025, 11, 6, 10, 30, 45)
}

# Serialize with datetime preservation
packed = msgpack.packb(data)

# Deserialize - datetimes are fully restored
restored = msgpack.unpackb(packed)

assert isinstance(restored['created_at'], datetime)
assert isinstance(restored['birth_date'], date)
assert restored['birth_date'] == date(1990, 5, 15)
```

### Decimal Numbers

```python
from decimal import Decimal
from rick.serializer import msgpack

# Financial data requiring precision
invoice = {
    'subtotal': Decimal('100.00'),
    'tax_rate': Decimal('0.085'),
    'tax': Decimal('8.50'),
    'total': Decimal('108.50')
}

packed = msgpack.packb(invoice)
restored = msgpack.unpackb(packed)

# Decimal precision is preserved
assert isinstance(restored['total'], Decimal)
assert restored['total'] == Decimal('108.50')
```

### UUID Objects

```python
from uuid import uuid4
from rick.serializer import msgpack

data = {
    'user_id': uuid4(),
    'session_id': uuid4(),
    'request_id': uuid4()
}

packed = msgpack.packb(data)
restored = msgpack.unpackb(packed)

# UUIDs are fully preserved
assert isinstance(restored['user_id'], uuid.UUID)
assert restored['user_id'] == data['user_id']
```

## Working with Dataclasses

The MessagePack serializer provides full dataclass support with automatic reconstruction:

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from rick.serializer.msgpack import msgpack


@dataclass
class Product:
    product_id: int
    name: str
    price: Decimal
    created_at: datetime


@dataclass
class Order:
    order_id: int
    customer_name: str
    products: list[Product]
    total: Decimal
    ordered_at: datetime


# Create complex nested structure
order = Order(
    order_id=1001,
    customer_name="John Doe",
    products=[
        Product(1, "Widget", Decimal("19.99"), datetime.now()),
        Product(2, "Gadget", Decimal("29.99"), datetime.now())
    ],
    total=Decimal("49.98"),
    ordered_at=datetime.now()
)

# Serialize
packed = msgpack.packb(order)

# Deserialize - full object reconstruction
restored = msgpack.unpackb(packed)

# Type and data are preserved
assert isinstance(restored, Order)
assert restored.order_id == 1001
assert isinstance(restored.products[0], Product)
assert isinstance(restored.products[0].price, Decimal)
assert isinstance(restored.products[0].created_at, datetime)
```

## Custom Objects

The serializer can handle custom Python objects:

```python
from datetime import datetime
from rick.serializer import msgpack


class UserSession:
    def __init__(self, user_id, username, login_time):
        self.user_id = user_id
        self.username = username
        self.login_time = login_time
        self.active = True


# Create instance
session = UserSession(123, "jdoe", datetime.now())

# Serialize
packed = msgpack.packb(session)

# Deserialize - object is reconstructed
restored = msgpack.unpackb(packed)

assert isinstance(restored, UserSession)
assert restored.user_id == 123
assert restored.username == "jdoe"
assert isinstance(restored.login_time, datetime)
```

**Important:** For custom objects to be reconstructable:

1. The class must be importable from the same module path
2. The class should have a no-argument `__new__()` method (most classes do)
3. Instance variables are restored via `setattr()`

## File I/O Operations

### Writing to Files

```python
from rick.serializer import msgpack
from datetime import datetime

data = {
    'version': '1.0',
    'created': datetime.now(),
    'records': [
        {'id': 1, 'value': 'first'},
        {'id': 2, 'value': 'second'}
    ]
}

# Write to file
with open('data.msgpack', 'wb') as f:
    msgpack.pack(data, f)
```

### Reading from Files

```python
from rick.serializer.msgpack import msgpack

# Read from file
with open('data.msgpack', 'rb') as f:
    data = msgpack.unpack(f)

print(data['version'])
print(data['created'])
```

## Caching Example

MessagePack is ideal for caching due to its compact size and speed:

```python
from rick.serializer import msgpack
from datetime import datetime, timedelta
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class CacheEntry:
    key: str
    value: dict
    created_at: datetime
    expires_at: datetime


class Cache:
    def __init__(self):
        self.storage = {}

    def set(self, key, value, ttl_seconds=3600):
        now = datetime.now()
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds)
        )
        # Serialize to bytes for storage
        self.storage[key] = msgpack.packb(entry)

    def get(self, key):
        if key not in self.storage:
            return None

        # Deserialize from bytes
        entry = msgpack.unpackb(self.storage[key])

        # Check expiration
        if datetime.now() > entry.expires_at:
            del self.storage[key]
            return None

        return entry.value


# Usage
cache = Cache()
cache.set('user:123', {
    'name': 'John Doe',
    'balance': Decimal('1000.50'),
    'last_login': datetime.now()
})

user_data = cache.get('user:123')
```

## Error Handling

### Serialization Errors

If an object type is not supported, a `TypeError` is raised:

```python
from rick.serializer import msgpack


class UnsupportedType:
    __slots__ = []  # No __dict__ and not a dataclass


try:
    msgpack.packb(UnsupportedType())
except TypeError as e:
    print(f"Cannot serialize: {e}")
    # Output: Cannot serialize: Unknown type: <class 'UnsupportedType'>
```

### Deserialization Errors

If a dataclass or custom object cannot be reconstructed, the serializer falls back to returning a dictionary with error
information:

```python
from dataclasses import dataclass
from rick.serializer import msgpack


@dataclass
class OriginalClass:
    value: int


# Serialize
data = OriginalClass(42)
packed = msgpack.packb(data)

# Simulate class no longer available (rename it)
OriginalClass.__name__ = "RenamedClass"

# Deserialize - reconstruction fails, returns dict
restored = msgpack.unpackb(packed)

# Check for reconstruction error
if isinstance(restored, dict) and '__reconstruction_error__' in restored:
    print(f"Reconstruction failed: {restored['__reconstruction_error__']}")
    print(f"Original class: {restored['__dataclass__']}")
    print(f"Data: {restored['value']}")
```

## Performance Comparison

Comparing MessagePack to JSON serialization:

```python
import json
import time
from datetime import datetime
from decimal import Decimal
from rick.serializer.json.json import ExtendedJsonEncoder
from rick.serializer import msgpack

# Create test data
data = {
    'records': [
        {
            'id': i,
            'timestamp': datetime.now(),
            'value': Decimal(f'{i}.99'),
            'active': True
        }
        for i in range(1000)
    ]
}

# JSON serialization
start = time.time()
json_data = json.dumps(data, cls=ExtendedJsonEncoder)
json_time = time.time() - start
json_size = len(json_data)

# MessagePack serialization
start = time.time()
msgpack_data = msgpack.packb(data)
msgpack_time = time.time() - start
msgpack_size = len(msgpack_data)

print(f"JSON: {json_size} bytes in {json_time:.4f}s")
print(f"MessagePack: {msgpack_size} bytes in {msgpack_time:.4f}s")
print(f"Size reduction: {(1 - msgpack_size / json_size) * 100:.1f}%")
print(f"Speed improvement: {(json_time / msgpack_time):.2f}x faster")
```

Typical results:

- MessagePack is 30-50% smaller
- MessagePack is 2-4x faster for serialization
- MessagePack is 3-5x faster for deserialization

## Binary Data Handling

```python
from rick.serializer import msgpack

data = {
    'filename': 'image.png',
    'content': b'\x89PNG\r\n\x1a\n...',  # Binary image data
    'view': memoryview(b'Memory buffer data')
}

# Binary data is efficiently stored
packed = msgpack.packb(data)
restored = msgpack.unpackb(packed)

assert isinstance(restored['content'], bytes)
assert isinstance(restored['view'], memoryview)
```


## How to handle Reconstruction Failures

```python
from rick.serializer.msgpack import msgpack


def safe_unpack(packed_data):
    result = msgpack.unpackb(packed_data)

    # Check if reconstruction failed
    if isinstance(result, dict):
        if '__reconstruction_error__' in result:
            print(f"Warning: Could not reconstruct {result.get('__dataclass__', result.get('__object__'))}")
            # Handle gracefully - use dict representation
            return result

    return result
```

## Security Considerations

When deserializing MessagePack data:

1. **Code Execution Risk:** The serializer dynamically imports modules and creates objects. Only deserialize data from
   trusted sources.

2. **Module Imports:** Dataclass and object reconstruction requires importing the original class. Ensure the module is
   available and safe.

## Limitations

1. **Class Availability:** Custom classes and dataclasses must be importable at deserialization time
2. **Circular References:** Not supported (like standard JSON)
3. **Class Evolution:** Changing a dataclass structure may cause deserialization issues
4. **Module Paths:** Class module paths must remain consistent

## Related Topics

- [JSON Serializer](json.md) - For human-readable serialization
- [Redis Cache](../resources/redis.md) - Uses serialization for caching
- [Forms](../forms/index.md) - For handling and validating incoming data
