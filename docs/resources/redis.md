# Redis Cache

Rick provides Redis-based caching implementations with support for custom serialization, encryption, and full Redis
client access. The module offers two cache classes: `RedisCache` for standard caching and `CryptRedisCache` for
encrypted caching of sensitive data.

**Location:** `rick.resource.redis`

## Overview

Redis caching in Rick provides:

- **Standardized Interface** - Implements `CacheInterface` for consistency
- **Flexible Serialization** - Support for pickle, JSON, MessagePack, or custom serializers
- **Encryption Support** - Built-in encrypted caching with Fernet256
- **Key Prefixing** - Namespace isolation for multiple applications or environments
- **TTL Support** - Automatic expiration of cached data
- **Full Client Access** - Direct access to underlying Redis client for advanced operations
- **Backend Wrapping** - Wrap existing Redis clients with cache interface

## RedisCache

Basic Redis cache implementation with pickle serialization by default.

**Location:** `rick.resource.redis.RedisCache`

### Constructor Parameters

```python
RedisCache(**kwargs)
```

**Redis Connection Parameters:**

| Parameter                  | Type           | Default     | Description                      |
|----------------------------|----------------|-------------|----------------------------------|
| `host`                     | str            | 'localhost' | Redis server hostname            |
| `port`                     | int            | 6379        | Redis server port                |
| `db`                       | int            | 0           | Redis database number            |
| `password`                 | str            | None        | Redis password                   |
| `socket_timeout`           | float          | None        | Socket timeout in seconds        |
| `socket_connect_timeout`   | float          | None        | Connection timeout in seconds    |
| `socket_keepalive`         | bool           | None        | Enable TCP keepalive             |
| `socket_keepalive_options` | dict           | None        | TCP keepalive options            |
| `connection_pool`          | ConnectionPool | None        | Custom connection pool           |
| `unix_socket_path`         | str            | None        | Unix socket path                 |
| `encoding`                 | str            | 'utf-8'     | String encoding                  |
| `encoding_errors`          | str            | 'strict'    | Encoding error handling          |
| `decode_responses`         | bool           | False       | Decode responses to strings      |
| `retry_on_timeout`         | bool           | False       | Retry on timeout                 |
| `ssl`                      | bool           | False       | Enable SSL                       |
| `ssl_keyfile`              | str            | None        | SSL key file path                |
| `ssl_certfile`             | str            | None        | SSL certificate file path        |
| `ssl_cert_reqs`            | str            | 'required'  | SSL certificate requirements     |
| `ssl_ca_certs`             | str            | None        | SSL CA certificates path         |
| `max_connections`          | int            | None        | Maximum connections in pool      |
| `single_connection_client` | bool           | False       | Use single connection            |
| `health_check_interval`    | int            | 0           | Health check interval in seconds |

**Cache-Specific Parameters:**

| Parameter      | Type        | Default      | Description                    |
|----------------|-------------|--------------|--------------------------------|
| `backend`      | redis.Redis | None         | Wrap existing Redis client     |
| `serializer`   | callable    | pickle.dumps | Function to serialize values   |
| `deserializer` | callable    | pickle.loads | Function to deserialize values |
| `prefix`       | str         | ""           | Key prefix for namespacing     |

### Methods

#### get(key)

Retrieve a value from the cache.

```python
value = cache.get('user:123')
```

**Parameters:**

- `key` (str) - Cache key

**Returns:** Cached value or `None` if not found

#### set(key, value, ttl=None)

Store a value in the cache.

```python
cache.set('user:123', user_data, ttl=3600)
```

**Parameters:**

- `key` (str) - Cache key
- `value` (any) - Value to cache (must be serializable)
- `ttl` (int, optional) - Time-to-live in seconds

**Returns:** True if successful

#### has(key)

Check if a key exists in the cache.

```python
if cache.has('user:123'):
    print("Key exists")
```

**Parameters:**

- `key` (str) - Cache key

**Returns:** `True` if key exists, `False` otherwise

#### remove(key)

Remove a key from the cache.

```python
cache.remove('user:123')
```

**Parameters:**

- `key` (str) - Cache key

**Returns:** `True` if key was removed, `False` if key didn't exist

#### purge()

Clear all keys from the current database.

```python
cache.purge()
```

**Warning:** This flushes the entire Redis database. Use with caution.

**Returns:** True if successful

#### client()

Get the underlying Redis client for advanced operations.

```python
redis_client = cache.client()
redis_client.pipeline()
```

**Returns:** `redis.Redis` instance

#### close()

Close the Redis connection.

```python
cache.close()
```

#### set_prefix(prefix)

Change the key prefix.

```python
cache.set_prefix('myapp:prod:')
```

**Parameters:**

- `prefix` (str) - New key prefix

## CryptRedisCache

Encrypted Redis cache implementation that extends `RedisCache` with automatic encryption/decryption using Fernet256.

**Location:** `rick.resource.redis.CryptRedisCache`

### Constructor Parameters

```python
CryptRedisCache(key, **kwargs)
```

**Required Parameter:**

| Parameter | Type | Description                                          |
|-----------|------|------------------------------------------------------|
| `key`     | str  | 64-character encryption key (will be base64 encoded) |

**Additional Parameters:** All parameters from `RedisCache` are supported.

**Important:** The encryption key must be exactly 64 characters long. The key is base64-encoded internally to create a
Fernet256 key.

### Generating Encryption Keys

```python
import secrets

# Generate a secure 64-character key
encryption_key = secrets.token_hex(32)  # Generates 64 hex characters
print(f"Key: {encryption_key}")
```

### Methods

`CryptRedisCache` inherits all methods from `RedisCache`. Values are automatically encrypted on `set()` and decrypted on
`get()`.

## Basic Usage Examples

### Simple Caching

```python
from rick.resource.redis import RedisCache

# Create cache instance
cache = RedisCache(host='localhost', port=6379, db=0)

# Store value
cache.set('greeting', 'Hello, World!')

# Retrieve value
message = cache.get('greeting')
print(message)  # Output: Hello, World!

# Check existence
if cache.has('greeting'):
    print("Key exists")

# Remove key
cache.remove('greeting')

# Close connection
cache.close()
```

### Caching with TTL

```python
from rick.resource.redis import RedisCache
from time import sleep

cache = RedisCache(host='localhost')

# Cache with 60-second expiration
cache.set('temp_data', {'status': 'processing'}, ttl=60)

# Data is available
print(cache.has('temp_data'))  # True

# Wait for expiration
sleep(61)

# Data is gone
print(cache.has('temp_data'))  # False
```

### Caching Complex Objects

```python
from rick.resource.redis import RedisCache
from datetime import datetime
from decimal import Decimal

cache = RedisCache(host='localhost')

# Cache complex data structures
user_data = {
    'id': 123,
    'name': 'John Doe',
    'balance': Decimal('1234.56'),
    'created_at': datetime.now(),
    'preferences': {
        'theme': 'dark',
        'notifications': True
    }
}

cache.set('user:123', user_data)
retrieved = cache.get('user:123')

# All types are preserved with pickle
assert isinstance(retrieved['balance'], Decimal)
assert isinstance(retrieved['created_at'], datetime)
```

### Using Key Prefixes

```python
from rick.resource.redis import RedisCache

# Create caches with different prefixes
dev_cache = RedisCache(host='localhost', prefix='dev:')
prod_cache = RedisCache(host='localhost', prefix='prod:')

# Same key, different namespaces
dev_cache.set('config', {'debug': True})
prod_cache.set('config', {'debug': False})

# Keys don't conflict
print(dev_cache.get('config'))  # {'debug': True}
print(prod_cache.get('config'))  # {'debug': False}
```

## Encrypted Caching

### Basic Encrypted Cache

```python
from rick.resource.redis import CryptRedisCache

# Create encrypted cache (key must be 64 characters)
cache = CryptRedisCache(
    key='0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
    host='localhost',
    port=6379
)

# Store sensitive data (automatically encrypted)
cache.set('api_token', {'token': 'secret123', 'expires': '2025-12-31'})

# Retrieve (automatically decrypted)
token = cache.get('api_token')
print(token)  # {'token': 'secret123', 'expires': '2025-12-31'}

cache.close()
```

### Encrypted Session Storage

```python
from rick.resource.redis import CryptRedisCache
from datetime import datetime
import secrets

# Generate encryption key
ENCRYPTION_KEY = secrets.token_hex(32)

# Create encrypted cache for sessions
session_cache = CryptRedisCache(
    key=ENCRYPTION_KEY,
    host='localhost',
    prefix='session:'
)

# Store session data securely
session_id = secrets.token_urlsafe(32)
session_data = {
    'user_id': 123,
    'username': 'jdoe',
    'roles': ['user', 'admin'],
    'created_at': datetime.now(),
    'csrf_token': secrets.token_hex(32)
}

# Store with 1-hour expiration
session_cache.set(session_id, session_data, ttl=3600)

# Retrieve session
session = session_cache.get(session_id)

# Data is decrypted automatically
print(session['username'])  # 'jdoe'
```

### Encrypted API Key Storage

```python
from rick.resource.redis import CryptRedisCache

# Cache for encrypted API keys
api_cache = CryptRedisCache(
    key='your-64-character-key-here-replace-with-actual-key-value-ok',
    host='localhost',
    db=1,
    prefix='api:keys:'
)

# Store API key securely
api_cache.set('service:github', {
    'api_key': 'ghp_xxxxxxxxxxxx',
    'api_secret': 'secret_value',
    'rate_limit': 5000
})

# Retrieve when needed
github_creds = api_cache.get('service:github')
```

## Custom Serialization

### Using MessagePack

```python
from rick.resource.redis import RedisCache
from rick.serializer.msgpack import msgpack
from datetime import datetime
from decimal import Decimal

# Create cache with MessagePack serialization
cache = RedisCache(
    host='localhost',
    serializer=msgpack.packb,
    deserializer=msgpack.unpackb
)

# MessagePack efficiently handles complex types
data = {
    'timestamp': datetime.now(),
    'amount': Decimal('999.99'),
    'status': 'active'
}

cache.set('transaction:001', data)
retrieved = cache.get('transaction:001')

# Types are preserved
assert isinstance(retrieved['timestamp'], datetime)
assert isinstance(retrieved['amount'], Decimal)
```

### Using JSON

```python
from rick.resource.redis import RedisCache
from rick.serializer.json.json import ExtendedJsonEncoder
import json
from datetime import datetime


# JSON serializer for interoperability
def json_serializer(obj):
    return json.dumps(obj, cls=ExtendedJsonEncoder).encode('utf-8')


def json_deserializer(data):
    # Note: JSON deserialization doesn't restore types
    return json.loads(data.decode('utf-8'))


cache = RedisCache(
    host='localhost',
    serializer=json_serializer,
    deserializer=json_deserializer
)

# Store data (types will be converted to JSON-compatible formats)
cache.set('data', {
    'timestamp': datetime.now(),  # Becomes ISO string
    'count': 42
})

retrieved = cache.get('data')
# Note: timestamp is now a string, not datetime
```

### Custom Serializer

```python
from rick.resource.redis import RedisCache
import json


class CustomSerializer:
    @staticmethod
    def serialize(obj):
        # Add metadata
        wrapped = {
            '_type': type(obj).__name__,
            '_data': obj
        }
        return json.dumps(wrapped).encode('utf-8')

    @staticmethod
    def deserialize(data):
        wrapped = json.loads(data.decode('utf-8'))
        return wrapped['_data']


cache = RedisCache(
    host='localhost',
    serializer=CustomSerializer.serialize,
    deserializer=CustomSerializer.deserialize
)

cache.set('custom', {'value': 42})
```

## Wrapping Existing Redis Client

### Basic Wrapping

```python
import redis
from rick.resource.redis import RedisCache

# Create your own Redis client with custom configuration
my_redis = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    max_connections=50,
    socket_keepalive=True
)

# Wrap with RedisCache interface
cache = RedisCache(backend=my_redis)

# Use cache interface
cache.set('key', 'value')

# Still have access to raw client
cache.client().info()
```

### With Connection Pool

```python
import redis
from rick.resource.redis import RedisCache

# Create custom connection pool
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=100,
    socket_keepalive=True,
    socket_connect_timeout=5
)

# Create Redis client with pool
redis_client = redis.Redis(connection_pool=pool)

# Wrap with cache interface
cache = RedisCache(backend=redis_client)
```

### Sentinel Configuration

```python
import redis
from redis.sentinel import Sentinel
from rick.resource.redis import RedisCache

# Setup Redis Sentinel
sentinel = Sentinel([
    ('sentinel1', 26379),
    ('sentinel2', 26379),
    ('sentinel3', 26379)
], socket_timeout=0.5)

# Get master client
master = sentinel.master_for('mymaster', socket_timeout=0.5)

# Wrap with RedisCache
cache = RedisCache(backend=master)
```

## Advanced Usage

### Pipeline Operations

```python
from rick.resource.redis import RedisCache

cache = RedisCache(host='localhost')

# Use pipeline for bulk operations
client = cache.client()
pipe = client.pipeline()

# Queue multiple operations
for i in range(100):
    pipe.set(f'key:{i}', f'value:{i}')

# Execute all at once
pipe.execute()
```

### Pub/Sub with Cache

```python
from rick.resource.redis import RedisCache

cache = RedisCache(host='localhost')
pubsub = cache.client().pubsub()

# Subscribe to channel
pubsub.subscribe('notifications')

# Publish message
cache.client().publish('notifications', 'New update available')

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
```

### Cache Statistics

```python
from rick.resource.redis import RedisCache

cache = RedisCache(host='localhost', prefix='myapp:')

# Get Redis info
info = cache.client().info()
print(f"Used memory: {info['used_memory_human']}")
print(f"Connected clients: {info['connected_clients']}")

# Get key count for namespace
keys = cache.client().keys('myapp:*')
print(f"Keys in namespace: {len(keys)}")
```

### Cache-Aside Pattern

```python
from rick.resource.redis import RedisCache

cache = RedisCache(host='localhost')


def get_user(user_id):
    """Cache-aside pattern implementation"""
    cache_key = f'user:{user_id}'

    # Try cache first
    user = cache.get(cache_key)

    if user is None:
        # Cache miss - load from database
        user = database.load_user(user_id)

        if user is not None:
            # Store in cache for 1 hour
            cache.set(cache_key, user, ttl=3600)

    return user


def update_user(user_id, user_data):
    """Update user and invalidate cache"""
    # Update database
    database.update_user(user_id, user_data)

    # Invalidate cache
    cache.remove(f'user:{user_id}')
```

### Write-Through Cache

```python
from rick.resource.redis import RedisCache

cache = RedisCache(host='localhost')


def save_user(user):
    """Write-through cache pattern"""
    # Write to database
    database.save_user(user)

    # Write to cache
    cache.set(f"user:{user['id']}", user, ttl=3600)


def get_user(user_id):
    """Always try cache first"""
    return cache.get(f'user:{user_id}')
```

### Rate Limiting

```python
from rick.resource.redis import RedisCache
from time import time

cache = RedisCache(host='localhost')


def rate_limit(user_id, max_requests=100, window=60):
    """Simple rate limiting with Redis"""
    key = f'rate_limit:{user_id}:{int(time() // window)}'

    # Get current count
    current = cache.get(key)

    if current is None:
        # First request in window
        cache.set(key, 1, ttl=window)
        return True

    if current >= max_requests:
        # Rate limit exceeded
        return False

    # Increment counter
    cache.client().incr(key)
    return True


# Usage
if rate_limit('user:123', max_requests=10, window=60):
    process_request()
else:
    raise RateLimitExceeded()
```

## Error Handling

### Connection Errors

```python
from rick.resource.redis import RedisCache
import redis

cache = RedisCache(host='localhost', port=6379)

try:
    cache.set('key', 'value')
except redis.ConnectionError as e:
    print(f"Cannot connect to Redis: {e}")
    # Fallback to alternative storage or raise
except redis.TimeoutError as e:
    print(f"Redis operation timed out: {e}")
    # Retry or use fallback
```

### Serialization Errors

```python
from rick.resource.redis import RedisCache
import pickle

cache = RedisCache(host='localhost')


class UnserializableObject:
    def __init__(self):
        self.file_handle = open('/tmp/test', 'w')  # Cannot pickle file handles


try:
    cache.set('bad_data', UnserializableObject())
except (pickle.PicklingError, TypeError) as e:
    print(f"Cannot serialize object: {e}")
```

### Graceful Degradation

```python
from rick.resource.redis import RedisCache
from rick.resource import CacheNull
import redis


def create_cache():
    """Create cache with fallback"""
    try:
        cache = RedisCache(host='localhost', port=6379, socket_connect_timeout=2)
        # Test connection
        cache.client().ping()
        return cache
    except (redis.ConnectionError, redis.TimeoutError):
        # Fallback to null cache (no-op)
        print("Warning: Redis unavailable, using null cache")
        return CacheNull()


# Use cache (works even if Redis is down)
cache = create_cache()
cache.set('key', 'value')  # No-op if Redis unavailable
```

## Troubleshooting

### Connection Issues

```python
# Test Redis connection
import redis

try:
    client = redis.Redis(host='localhost', port=6379, socket_connect_timeout=5)
    client.ping()
    print("Connection successful")
except redis.ConnectionError:
    print("Cannot connect to Redis")
```

### Memory Issues

```python
# Check memory usage
cache = RedisCache(host='localhost')
info = cache.client().info('memory')
print(f"Used memory: {info['used_memory_human']}")
print(f"Peak memory: {info['used_memory_peak_human']}")

# Set maxmemory policy in redis.conf:
# maxmemory 256mb
# maxmemory-policy allkeys-lru
```

### Key Expiration Issues

```python
# Check TTL
cache = RedisCache(host='localhost')
ttl = cache.client().ttl('mykey')

if ttl == -1:
    print("Key exists but has no expiration")
elif ttl == -2:
    print("Key does not exist")
else:
    print(f"Key expires in {ttl} seconds")
```

## Related Topics

- [Serializers](../serializers/index.md) - Efficient data serialization options
- [Crypto](../crypto/index.md) - Encryption utilities used by CryptRedisCache
- [Configuration](config.md) - Loading Redis configuration from files
