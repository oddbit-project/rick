# JSON Serializer

The JSON serializer in Rick extends Python's built-in `json` module with support for additional Python types commonly
used in applications.

## Available Encoders

Rick provides two JSON encoder classes:

### ExtendedJsonEncoder

A general-purpose JSON encoder that preserves field naming conventions (snake_case).

**Location:** `rick.serializer.json.ExtendedJsonEncoder`

### CamelCaseJsonEncoder

A specialized JSON encoder that converts Python snake_case field names to JavaScript-friendly camelCase.

**Location:** `rick.serializer.json.CamelCaseJsonEncoder`

## Supported Types

Both encoders support the following Python types:

| Type                      | Serialization Method                     |
|---------------------------|------------------------------------------|
| `datetime.date`           | ISO 8601 format string via `isoformat()` |
| `datetime.datetime`       | ISO 8601 format string via `isoformat()` |
| `decimal.Decimal`         | String representation                    |
| `uuid.UUID`               | String representation                    |
| Dataclasses               | Dictionary via `dataclasses.asdict()`    |
| Objects with `__html__()` | String via `str(__html__())`             |
| Objects with `asdict()`   | Dictionary via `obj.asdict()`            |
| `memoryview`              | UTF-8 decoded string                     |
| `bytes`                   | UTF-8 decoded string                     |
| Objects with `__dict__`   | Dictionary via `obj.__dict__`            |

## Basic Usage

### Using ExtendedJsonEncoder

```python
import json
import datetime
import decimal
import uuid
from dataclasses import dataclass
from rick.serializer.json.json import ExtendedJsonEncoder

# Create data with complex types
data = {
    'id': uuid.uuid4(),
    'created_at': datetime.datetime.now(),
    'modified_date': datetime.date.today(),
    'price': decimal.Decimal('99.99'),
    'quantity': 5
}

# Serialize to JSON string
json_string = json.dumps(data, cls=ExtendedJsonEncoder)
print(json_string)

# Serialize to file
with open('data.json', 'w') as f:
    json.dump(data, f, cls=ExtendedJsonEncoder, indent=2)
```

**Output:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-11-06T10:30:45.123456",
  "modified_date": "2025-11-06",
  "price": "99.99",
  "quantity": 5
}
```

### Using CamelCaseJsonEncoder

```python
import json
from dataclasses import dataclass
from rick.serializer.json.json import CamelCaseJsonEncoder


@dataclass
class UserProfile:
    user_id: int
    first_name: str
    last_name: str
    email_address: str
    is_active: bool


profile = UserProfile(
    user_id=123,
    first_name="John",
    last_name="Doe",
    email_address="john.doe@example.com",
    is_active=True
)

# Convert to camelCase JSON
json_string = json.dumps(profile, cls=CamelCaseJsonEncoder)
print(json_string)
```

**Output:**

```json
{
  "userId": 123,
  "firstName": "John",
  "lastName": "Doe",
  "emailAddress": "john.doe@example.com",
  "isActive": true
}
```

## Working with Dataclasses

Both encoders have excellent support for dataclasses:

```python
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from rick.serializer.json.json import ExtendedJsonEncoder


@dataclass
class Product:
    product_id: int
    name: str
    price: Decimal
    created_at: datetime


@dataclass
class Order:
    order_id: int
    products: list[Product]
    total: Decimal


# Create nested dataclass structure
order = Order(
    order_id=1001,
    products=[
        Product(1, "Widget", Decimal("19.99"), datetime.now()),
        Product(2, "Gadget", Decimal("29.99"), datetime.now())
    ],
    total=Decimal("49.98")
)

# Serialize nested dataclasses
result = json.dumps(order, cls=ExtendedJsonEncoder, indent=2)
print(result)
```

## Custom Objects

The encoder can handle custom objects with `__dict__` attributes:

```python
import json
from datetime import datetime
from rick.serializer.json.json import ExtendedJsonEncoder


class CustomObject:
    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at
        self.internal_id = id(self)


obj = CustomObject("test", datetime.now())
result = json.dumps(obj, cls=ExtendedJsonEncoder)
print(result)
```

## Objects with asdict() Method

If your object implements an `asdict()` method, the encoder will use it:

```python
import json
from rick.serializer.json.json import ExtendedJsonEncoder


class CustomSerializable:
    def __init__(self, value):
        self._value = value
        self._internal = "hidden"

    def asdict(self):
        # Control exactly what gets serialized
        return {
            'value': self._value,
            'type': self.__class__.__name__
        }


obj = CustomSerializable(42)
result = json.dumps(obj, cls=ExtendedJsonEncoder)
print(result)
# Output: {"value": 42, "type": "CustomSerializable"}
```

## HTML Objects

Objects with `__html__()` method are serialized via their HTML representation:

```python
import json
from rick.serializer.json.json import ExtendedJsonEncoder


class HTMLWidget:
    def __init__(self, content):
        self.content = content

    def __html__(self):
        return f"<div>{self.content}</div>"


widget = HTMLWidget("Hello World")
result = json.dumps({'widget': widget}, cls=ExtendedJsonEncoder)
print(result)
# Output: {"widget": "<div>Hello World</div>"}
```

## Working with Binary Data

Both encoders can handle binary data types:

```python
import json
from rick.serializer.json.json import ExtendedJsonEncoder

data = {
    'binary': b'Hello, World!',
    'memory': memoryview(b'Memory data')
}

result = json.dumps(data, cls=ExtendedJsonEncoder)
print(result)
# Output: {"binary": "Hello, World!", "memory": "Memory data"}
```

## API Response Example

A complete example for building API responses:

```python
import json
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from uuid import uuid4
from rick.serializer.json.json import CamelCaseJsonEncoder


@dataclass
class ApiResponse:
    request_id: str
    timestamp: datetime
    success: bool
    data: dict
    error_message: str | None = None


def create_api_response(data, success=True, error=None):
    response = ApiResponse(
        request_id=str(uuid4()),
        timestamp=datetime.now(),
        success=success,
        data=data,
        error_message=error
    )
    return json.dumps(response, cls=CamelCaseJsonEncoder, indent=2)


# Success response
result = create_api_response({
    'user_count': 150,
    'total_revenue': Decimal('12345.67')
})
print(result)
```

**Output:**

```json
{
  "requestId": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-11-06T10:30:45.123456",
  "success": true,
  "data": {
    "userCount": 150,
    "totalRevenue": "12345.67"
  },
  "errorMessage": null
}
```

## Error Handling

If an object cannot be serialized, the encoder raises a `RuntimeError`:

```python
import json
from rick.serializer.json.json import ExtendedJsonEncoder


class UnserializableObject:
    __slots__ = ['value']  # No __dict__

    def __init__(self, value):
        self.value = value


try:
    obj = UnserializableObject(42)
    json.dumps(obj, cls=ExtendedJsonEncoder)
except RuntimeError as e:
    print(f"Serialization error: {e}")
    # Output: Serialization error: cannot serialize type '<class 'UnserializableObject'>' to Json
```

## Deserialization Note

The Rick JSON encoders handle serialization (Python to JSON) only. For deserialization (JSON to Python), you'll need to:

1. Use standard `json.loads()` to get dictionaries
2. Manually convert strings back to complex types (datetime, Decimal, UUID)
3. Reconstruct dataclasses or custom objects as needed

Example deserialization:

```python
import json
from datetime import datetime
from decimal import Decimal
from uuid import UUID

json_string = '{"id": "550e8400-e29b-41d4-a716-446655440000", "created_at": "2025-11-06T10:30:45.123456", "price": "99.99"}'

# Parse JSON
data = json.loads(json_string)

# Convert back to typed objects
data['id'] = UUID(data['id'])
data['created_at'] = datetime.fromisoformat(data['created_at'])
data['price'] = Decimal(data['price'])
```

## Related Topics

- [MessagePack Serializer](msgpack.md) - For binary serialization with bidirectional support
- [Validators](../validators/index.md) - For validating deserialized data
- [Forms](../forms/index.md) - For handling request data with validation
