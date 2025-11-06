# Resources

Rick provides resource management components for working with external systems and services. These components offer
standardized interfaces and utilities for common operations like caching, configuration management, file operations, and
stream processing.

## Overview

The resource module includes components for:

- **Caching** - Redis-based caching with optional encryption
- **Configuration** - Environment variables, JSON, TOML, and hybrid configuration loaders
- **File Operations** - File handling utilities
- **Stream Processing** - Multipart stream reading and processing
- **Console Output** - Colored console output and formatting

## Cache Interface

All cache implementations in Rick follow the `CacheInterface` protocol:

```python
from rick.resource import CacheInterface


class CacheInterface:
    def get(self, key):
        """Retrieve value by key"""
        pass

    def set(self, key, value, ttl=None):
        """Store value with optional TTL (time-to-live)"""
        pass

    def has(self, key):
        """Check if key exists"""
        pass

    def remove(self, key):
        """Remove key"""
        pass

    def purge(self):
        """Clear all cached data"""
        pass

    def set_prefix(self, prefix):
        """Set key prefix for namespacing"""
        pass
```

This standardized interface allows you to swap cache implementations without changing your application code.

## Available Resources

### Redis Cache

Rick provides two Redis cache implementations:

- **[RedisCache](redis.md#rediscache)** - Basic Redis caching with pickle serialization
- **[CryptRedisCache](redis.md#cryptrediscache)** - Encrypted Redis cache for sensitive data

Features:

- Full Redis client access for advanced operations
- Configurable serialization (pickle, JSON, MessagePack, etc.)
- Key prefixing for namespace isolation
- TTL (time-to-live) support
- Connection pooling and SSL support
- Backend wrapping of existing Redis clients

[Read full Redis documentation](redis.md)

### Configuration Loaders

Rick provides multiple configuration loaders:

- **[EnvironmentConfig](config.md#environmentconfig)** - Load configuration from environment variables with type conversion
- **[JsonFileConfig](config.md#jsonfileconfig)** - Load configuration from JSON files
- **[TomlFileConfig](config.md#tomlfileconfig)** - Load configuration from TOML files
- **[HybridFileConfig](config.md#hybridfileconfig)** - Auto-detect file format (JSON or TOML)

Features:

- Automatic type conversion based on default values
- Custom validation functions with `validate_*` methods
- Default values with file/environment overrides
- StrOrFile wrapper for loading secrets from files
- Nested configuration support
- Configuration reload without restart
- Prefix support for environment variable namespacing

[Read full Configuration documentation](config.md)

### File Operations

Utilities for common file operations:

- File reading and writing
- Path manipulation
- Directory traversal
- File metadata handling

### Stream Processing

Rick provides stream processing utilities for handling multipart data streams:

- **[MultiPartReader](stream.md#multipartreader)** - Combine multiple data sources into a seekable stream
- **[FileSlice](stream.md#fileslice)** - Read file slices from disk
- **[BytesIOSlice](stream.md#bytesioslice)** - Read slices from memory buffers

Features:

- Minimal memory usage for large files
- Seek support for random access
- Combine files, buffers, and custom sources
- Stream processing with efficient chunking
- Custom slice implementations

[Read full Stream Processing documentation](stream.md)

### Console Output

Rick provides utilities for colored and formatted console output:

- **[AnsiColor](console.md#ansicolor)** - ANSI color formatting with 16 colors and text attributes
- **[ConsoleWriter](console.md#consolewriter)** - High-level console writer with semantic methods

Features:

- 16 foreground and background colors (standard and light variants)
- Text attributes (bold, dim, underline, reversed)
- Semantic output methods (success, error, warning, header)
- Separate stdout and stderr streams
- Custom colorization and styling

[Read full Console Output documentation](console.md)

## Common Use Cases

### Colored Console Output

```python
from rick.resource.console import ConsoleWriter, AnsiColor

# High-level semantic output
console = ConsoleWriter()
console.header('Application Startup')
console.success('Database connection established')
console.warn('Cache is disabled')
console.error('Failed to load plugin')

# Low-level color formatting
color = AnsiColor()
print(color.red('Error message', attr='bold'))
print(color.green('Success', 'white', ['bold', 'underline']))
print(color.blue('[INFO]', attr='bold') + ' Application started')
```

### CLI Progress Output

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()

steps = ['Loading config', 'Connecting DB', 'Starting services']

for step in steps:
    console.write(f'{step}...', eol=False)
    # Do work...
    console.success(' Done')

console.write('')
console.success('Application ready')
```

## Next Steps

- Explore [Redis Cache](redis.md) for detailed caching documentation
- Learn about [Configuration](config.md) for configuration management
- Check [Console Output](console.md) for CLI formatting
- Review [Serializers](../serializers/index.md) for efficient data encoding
