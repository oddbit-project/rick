# Welcome to Rick

[![Tests](https://github.com/oddbit-project/rick/workflows/Tests/badge.svg?branch=master)](https://github.com/oddbit-project/rick/actions)
[![pypi](https://img.shields.io/pypi/v/rick.svg)](https://pypi.org/project/rick/)
[![license](https://img.shields.io/pypi/l/rick.svg)](https://git.oddbit.org/OddBit/rick/src/branch/master/LICENSE)

Rick is a comprehensive plumbing library for building microframework-based Python applications. It provides essential building blocks and utilities for constructing robust, maintainable applications without imposing architectural constraints.

**What Rick Is:**
- A collection of battle-tested utilities and components
- Foundation for building custom frameworks and applications
- Lightweight and modular with minimal dependencies
- Python 3.10+ compatible

**What Rick Is Not:**
- Not a web framework (no HTTP/WSGI/ASGI functionality)
- Not a database ORM (use [RickDb](https://git.oddbit.org/OddBit/rick_db) for database operations)
- Not opinionated about application structure

## Core Philosophy

Rick follows these principles:

1. **Modularity** - Use only what you need
2. **Simplicity** - Clear, straightforward APIs
3. **Flexibility** - Adapt to your architecture, not the other way around
4. **Reliability** - Comprehensive test coverage and type support
5. **Performance** - Efficient implementations with minimal overhead

## Quick Start

### Installation

```bash
pip install rick
```

### Basic Example

```python
from rick.base import Di
from rick.form import RequestRecord, Field
from rick.resource.config import EnvironmentConfig
from rick.resource.redis import RedisCache

# Dependency Injection
di = Di()
di.add('cache', RedisCache(host='localhost'))
cache = di.get('cache')

# Form Validation
class UserForm(RequestRecord):
    def __init__(self):
        super().__init__()
        self.field('email', validators='required|email')
        self.field('password', validators='required|minlen:8')

form = UserForm()
if form.is_valid({'email': 'user@example.com', 'password': 'secret123'}):
    print("Valid!")

# Configuration
class AppConfig(EnvironmentConfig):
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DEBUG = False

config = AppConfig().build()
```

## Components

### Core Components

#### [Base Classes](forms/index.md)
- **Dependency Injection (Di)** - Service container with singleton and factory patterns
- **Container Classes** - Immutable and mutable data containers
- **Registry** - Thread-safe class registration and retrieval
- **MapLoader** - Dynamic class loading and instantiation

#### [Forms and Validation](forms/index.md)
- **[RequestRecord](forms/requests.md)** - Request validation with nested record support
- **[Form](forms/form.class.md)** - Full-featured forms with fieldsets and controls
- **Field** - Field definitions with validators and filters
- **[30+ Validators](validators/validator_list.md)** - Email, IP, UUID, numeric, string validators
- **[Filters](filters/index.md)** - Input transformation and sanitization

### Serialization

#### [Serializers](serializers/index.md)
- **[JSON Serializer](serializers/json.md)** - Extended JSON encoding with Python type support
  - ExtendedJsonEncoder for standard serialization
  - CamelCaseJsonEncoder for JavaScript compatibility
  - Supports datetime, Decimal, UUID, dataclasses
- **[MessagePack Serializer](serializers/msgpack.md)** - Binary serialization with full type preservation
  - Bidirectional encoding/decoding
  - 30-50% smaller than JSON
  - 2-4x faster serialization
  - Full support for custom objects and dataclasses

### Resources

#### [Configuration Management](resources/config.md)
- **[EnvironmentConfig](resources/config.md#environmentconfig)** - Environment variable loading with type conversion
- **[JsonFileConfig](resources/config.md#jsonfileconfig)** - JSON configuration files
- **[TomlFileConfig](resources/config.md#tomlfileconfig)** - TOML configuration files
- **[HybridFileConfig](resources/config.md#hybridfileconfig)** - Auto-detect JSON or TOML
- Custom validation functions
- StrOrFile wrapper for loading secrets from files

#### [Caching](resources/redis.md)
- **[RedisCache](resources/redis.md#rediscache)** - Redis caching with pickle serialization
- **[CryptRedisCache](resources/redis.md#cryptrediscache)** - Encrypted Redis cache with Fernet256
- Custom serialization support (pickle, JSON, MessagePack)
- Key prefixing for namespace isolation
- TTL support for automatic expiration
- Full Redis client access for advanced operations

#### [Console Output](resources/console.md)
- **[AnsiColor](resources/console.md#ansicolor)** - ANSI color formatting with 16 colors
- **[ConsoleWriter](resources/console.md#consolewriter)** - High-level console writer
- Semantic output methods (success, error, warning, header)
- Text attributes (bold, dim, underline, reversed)
- Separate stdout and stderr streams

#### Other Resources
- **Event Manager** - Event dispatching and handling
- **Stream Processing** - MultiPartReader for multipart/form-data
- **File Operations** - File handling utilities

### Security and Cryptography

#### [Crypto](resources/redis.md)
- **Fernet256** - 256-bit encryption (adapted from cryptography library)
- **MultiFernet256** - Multi-key encryption support
- **BCrypt** - Password hashing
- **Buffer Utilities** - Hash functions (SHA1, SHA256, SHA512)

### Mixins

- **Injectable** - Dependency injection integration
- **Runnable** - Runnable interface for services
- **[Translator](mixins/translator.class.md)** - Internationalization and localization support

## Feature Highlights

### Dependency Injection

```python
from rick.base import Di

# Create DI container
di = Di()

# Register singleton
di.add('config', config_instance)

# Register factory
def create_logger(di_instance):
    return {'name': 'logger'}

di.add('logger', create_logger)

# Retrieve services
config = di.get('config')
logger = di.get('logger')
```

### Form Validation

```python
from rick.form import RequestRecord

class RegistrationForm(RequestRecord):
    def __init__(self):
        super().__init__()
        self.field('username', validators='required|alphanum|minlen:3')
        self.field('email', validators='required|email')
        self.field('password', validators='required|minlen:8')
        self.field('age', validators='required|int|between:18,120')

    def validate_username(self, data, field):
        # Custom validation
        if data['username'] in ['admin', 'root']:
            self.add_error('username', 'Username not allowed')
            return False
        return True

form = RegistrationForm()
if form.is_valid(request_data):
    # Process valid data
    user_data = form.get_data()
else:
    # Handle errors
    errors = form.get_errors()
```

### Configuration Management

```python
from rick.resource.config import EnvironmentConfig, StrOrFile

class ProductionConfig(EnvironmentConfig):
    # Database settings
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_PASSWORD = StrOrFile(None)  # Load from file

    # Application settings
    DEBUG = False
    SECRET_KEY = StrOrFile(None)
    MAX_WORKERS = 4

    def validate_database(self, data: dict):
        """Ensure database is properly configured"""
        if not data.get('db_host'):
            raise ValueError("Database host is required")

# Environment variables override defaults
# export DB_HOST=production-server
# export DB_PASSWORD=/secrets/db-password.txt

config = ProductionConfig().build()
```

### Redis Caching

```python
from rick.resource.redis import RedisCache, CryptRedisCache
from rick.serializer.msgpack import msgpack

# Standard cache with MessagePack
cache = RedisCache(
    host='localhost',
    serializer=msgpack.packb,
    deserializer=msgpack.unpackb,
    prefix='myapp:'
)

cache.set('user:123', user_data, ttl=3600)
user = cache.get('user:123')

# Encrypted cache for sensitive data
secure_cache = CryptRedisCache(
    key='your-64-character-encryption-key-here-must-be-exactly-64ch',
    host='localhost'
)

secure_cache.set('api_token', {'token': 'secret123'})
```

### Serialization

```python
from rick.serializer.json.json import ExtendedJsonEncoder, CamelCaseJsonEncoder
from rick.serializer.msgpack import msgpack
import json
from datetime import datetime
from decimal import Decimal

# JSON serialization
data = {
    'timestamp': datetime.now(),
    'amount': Decimal('123.45'),
    'status': 'active'
}

# Standard JSON
json_str = json.dumps(data, cls=ExtendedJsonEncoder)

# CamelCase for JavaScript
json_str = json.dumps(data, cls=CamelCaseJsonEncoder)

# MessagePack - faster and smaller
packed = msgpack.packb(data)
restored = msgpack.unpackb(packed)  # Full type preservation
```

### Console Output

```python
from rick.resource.console import ConsoleWriter, AnsiColor

# High-level semantic output
console = ConsoleWriter()
console.header('Application Startup')
console.success('Database connected')
console.warn('Cache disabled')
console.error('Plugin failed to load')

# Low-level color formatting
color = AnsiColor()
print(color.red('Error:', attr='bold') + ' Operation failed')
print(color.green('Success', 'white', ['bold', 'underline']))
```

## Architecture Pattern

Rick follows a modular architecture where each component is independent:

```
rick/
├── base/          # DI, Registry, Containers
├── form/          # Forms and RequestRecord
├── validator/     # Validation rules
├── filter/        # Input filters
├── serializer/    # JSON and MessagePack
├── resource/      # External resources
│   ├── config/    # Configuration loaders
│   ├── redis/     # Redis caching
│   ├── console/   # Console output
│   └── stream/    # Stream processing
├── crypto/        # Encryption utilities
├── event/         # Event system
├── mixin/         # Reusable mixins
└── util/          # General utilities
```

## Documentation Structure

- **[Forms](forms/index.md)** - Form handling and request validation
- **[Validators](validators/index.md)** - Available validation rules
- **[Serializers](serializers/index.md)** - JSON and MessagePack serialization
- **[Resources](resources/index.md)** - Caching, configuration, console, and more
- **[Mixins](mixins/translator.class.md)** - Translation and other mixins


## Related Projects

- **[RickDb](https://git.oddbit.org/OddBit/rick_db)** - Database abstraction layer
- **[Flask](https://flask.palletsprojects.com)** - Web framework (recommended for HTTP functionality)

Rick is released under an open-source license. See the [LICENSE](https://git.oddbit.org/OddBit/rick/src/branch/master/LICENSE) file for details.

## Getting Started

1. **[Request Validation](forms/requests.md)** - Validate incoming requests
2. **[Configuration Management](resources/config.md)** - Load and validate configuration
3. **[Redis Caching](resources/redis.md)** - Implement caching strategies
4. **[Serialization](serializers/index.md)** - Efficient data encoding
5. **[Console Output](resources/console.md)** - Build beautiful CLI applications
