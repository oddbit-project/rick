# Configuration Loaders

Rick provides flexible configuration loading utilities for managing application settings from multiple sources. The
configuration module supports environment variables, JSON files, TOML files, and hybrid configurations with validation
and type conversion.

**Location:** `rick.resource.config`

## Overview

Configuration management in Rick provides:

- **Environment Variable Loading** - Load settings from environment variables with type conversion
- **File-Based Configuration** - Load from JSON or TOML files
- **Default Values** - Define fallback values for missing configuration
- **Validation** - Custom validation functions to ensure configuration correctness
- **Type Conversion** - Automatic type conversion based on default values
- **Hybrid Loading** - Auto-detect file format or combine multiple sources
- **StrOrFile Support** - Load values from files when needed

## Available Configuration Loaders

### EnvironmentConfig

Load configuration from environment variables with automatic type conversion.

**Location:** `rick.resource.config.EnvironmentConfig`

### JsonFileConfig

Load configuration from JSON files with validation support.

**Location:** `rick.resource.config.JsonFileConfig`

### TomlFileConfig

Load configuration from TOML files with validation support.

**Location:** `rick.resource.config.TomlFileConfig`

### HybridFileConfig

Auto-detect file format (JSON or TOML) based on file extension.

**Location:** `rick.resource.config.HybridFileConfig`

## EnvironmentConfig

### Overview

`EnvironmentConfig` loads configuration from environment variables with automatic type conversion. Class attributes
defined in uppercase are mapped to environment variables and converted to lowercase keys in the resulting configuration.

### Features

- Automatic type conversion (str, int, bool, list, dict)
- Environment variable override of default values
- Optional validation functions
- Prefix support for namespacing
- StrOrFile wrapper for loading values from files

### Basic Usage

```python
from rick.resource.config import EnvironmentConfig


class DatabaseConfig(EnvironmentConfig):
    # Define configuration with default values
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'myapp'
    DB_USERNAME = 'postgres'
    DB_PASSWORD = 'password'
    DB_SSL = False


# Build configuration (environment variables override defaults)
config = DatabaseConfig().build()

# Access configuration (keys are lowercase)
print(config.db_host)  # 'localhost' or value from DB_HOST env var
print(config.db_port)  # 5432 or value from DB_PORT env var
print(config.db_ssl)  # False or value from DB_SSL env var
```

### Type Conversion

Environment variables are automatically converted to the type of the default value:

```python
from rick.resource.config import EnvironmentConfig


class AppConfig(EnvironmentConfig):
    # Type hints via default values
    API_KEY = None  # str - None defaults to string
    DEBUG_MODE = False  # bool - converted from env var
    MAX_WORKERS = 4  # int - parsed from env string
    ALLOWED_HOSTS = []  # list - split by comma separator
    FEATURE_FLAGS = {}  # dict - parsed as JSON


# Set environment variables:
# export DEBUG_MODE=true
# export MAX_WORKERS=8
# export ALLOWED_HOSTS=localhost,127.0.0.1,example.com
# export FEATURE_FLAGS='{"new_ui": true, "beta_features": false}'

config = AppConfig().build()

print(config.debug_mode)  # True (bool)
print(config.max_workers)  # 8 (int)
print(config.allowed_hosts)  # ['localhost', '127.0.0.1', 'example.com']
print(config.feature_flags)  # {'new_ui': True, 'beta_features': False}
```

### Supported Types

| Default Type | Environment Value | Result Type | Example          |
|--------------|-------------------|-------------|------------------|
| `None`       | Any string        | `str`       | `"value"`        |
| `""`         | Any string        | `str`       | `"hello"`        |
| `0`          | Numeric string    | `int`       | `42`             |
| `False`      | Bool string       | `bool`      | `True`           |
| `[]`         | Comma-separated   | `list`      | `['a', 'b']`     |
| `{}`         | JSON string       | `dict`      | `{'key': 'val'}` |

### Custom List Separator

```python
from rick.resource.config import EnvironmentConfig


class CustomConfig(EnvironmentConfig):
    # Change list separator from comma to semicolon
    list_separator = ";"

    SERVERS = []


# export SERVERS=server1;server2;server3
config = CustomConfig().build()
print(config.servers)  # ['server1', 'server2', 'server3']
```

### Validation

Add custom validation by defining methods that start with `validate_`:

```python
from rick.resource.config import EnvironmentConfig


class ValidatedConfig(EnvironmentConfig):
    DB_HOST = 'localhost'
    DB_PORT = 5432
    API_KEY = None
    MAX_CONNECTIONS = 10

    def validate_database(self, data: dict):
        """Validate database configuration"""
        if not data.get('db_host'):
            raise ValueError("Database host is required")

        port = data.get('db_port', 0)
        if not (1 <= port <= 65535):
            raise ValueError("Database port must be between 1 and 65535")

    def validate_api_key(self, data: dict):
        """Validate API key format"""
        api_key = data.get('api_key')
        if not api_key:
            raise ValueError("API key is required")

        if len(api_key) < 32:
            raise ValueError("API key must be at least 32 characters")

    def validate_connections(self, data: dict):
        """Validate connection pool settings"""
        max_conn = data.get('max_connections', 0)
        if max_conn <= 0:
            raise ValueError("Max connections must be positive")


# Will raise ValueError if validation fails
config = ValidatedConfig().build()
```

### Prefix Support

Use prefixes to namespace environment variables:

```python
from rick.resource.config import EnvironmentConfig


class PrefixedConfig(EnvironmentConfig):
    DB_HOST = 'localhost'
    DB_PORT = 5432
    API_KEY = None


# Set environment variables with prefix:
# export MYAPP_DB_HOST=production-server
# export MYAPP_DB_PORT=3306
# export MYAPP_API_KEY=secret123

# Build with prefix
config = PrefixedConfig().build(prefix="MYAPP_")

print(config.db_host)  # 'production-server'
print(config.db_port)  # 3306
```

### StrOrFile Wrapper

Load values from files when environment variable points to a file path:

```python
from rick.resource.config import EnvironmentConfig, StrOrFile


class SecureConfig(EnvironmentConfig):
    API_KEY = StrOrFile(None)
    DB_PASSWORD = StrOrFile(None)


# Set environment variables:
# export API_KEY=/secrets/api-key.txt
# export DB_PASSWORD=plaintext_password

# Build configuration
config = SecureConfig().build()

# If API_KEY starts with '/' or './', content is read from file
# Otherwise, the value is used as-is
print(config.api_key)  # Content of /secrets/api-key.txt
print(config.db_password)  # "plaintext_password"
```

**StrOrFile Rules:**

- If value starts with `/` or `./`, it's treated as a file path
- File content is read and whitespace is stripped
- If file doesn't exist, `ValueError` is raised (unless `silent=True`)
- Use `StrOrFile(value, silent=True)` to return value as-is if file missing

### Complete Example

```python
import os
from rick.resource.config import EnvironmentConfig, StrOrFile


class ProductionConfig(EnvironmentConfig):
    # Database settings
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'production'
    DB_USER = 'postgres'
    DB_PASSWORD = StrOrFile(None)

    # Application settings
    DEBUG = False
    SECRET_KEY = StrOrFile(None)
    ALLOWED_HOSTS = []

    # Feature flags
    ENABLE_CACHING = True
    ENABLE_MONITORING = True
    MAX_UPLOAD_SIZE = 10485760  # 10MB in bytes

    # API configuration
    API_RATE_LIMIT = 100
    API_TIMEOUT = 30

    def validate_database(self, data: dict):
        """Ensure database is properly configured"""
        required = ['db_host', 'db_name', 'db_user', 'db_password']
        for field in required:
            if not data.get(field):
                raise ValueError(f"Database configuration missing: {field}")

    def validate_security(self, data: dict):
        """Ensure security settings are production-ready"""
        if data.get('debug'):
            raise ValueError("DEBUG must be False in production")

        if not data.get('secret_key'):
            raise ValueError("SECRET_KEY is required")

        if len(data.get('secret_key', '')) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")

    def validate_rate_limit(self, data: dict):
        """Validate rate limiting configuration"""
        rate_limit = data.get('api_rate_limit', 0)
        if rate_limit <= 0:
            raise ValueError("API rate limit must be positive")


# Set environment variables
os.environ['DB_PASSWORD'] = '/secrets/db-password.txt'
os.environ['SECRET_KEY'] = '/secrets/secret-key.txt'
os.environ['ALLOWED_HOSTS'] = 'api.example.com,www.example.com'

# Build and validate configuration
config = ProductionConfig().build()

# Use configuration
print(f"Connecting to {config.db_host}:{config.db_port}/{config.db_name}")
```

## JsonFileConfig

### Overview

`JsonFileConfig` loads configuration from JSON files with support for default values, validation, and runtime
overrides.

### Basic Usage

```python
from rick.resource.config import JsonFileConfig


class DatabaseConfig(JsonFileConfig):
    # Default values
    db_host = "localhost"
    db_port = 5432
    db_name = "myapp"
    api_key = None
    debug = False


# Load from file (values in file override defaults)
config = DatabaseConfig("config.json").build()

print(config.db_host)  # Value from config.json or default
print(config.db_port)  # Value from config.json or default
```

### Example JSON File

**config.json:**

```json
{
  "db_host": "production-server.example.com",
  "db_port": 3306,
  "db_name": "production_db",
  "api_key": "prod_api_key_1234567890abcdef",
  "debug": false,
  "features": {
    "enable_caching": true,
    "max_connections": 100
  }
}
```

### With Validation

```python
from rick.resource.config import JsonFileConfig


class ValidatedConfig(JsonFileConfig):
    db_host = "localhost"
    db_port = 5432
    api_key = None

    def validate_database(self, data: dict):
        """Validate database configuration"""
        if not data.get('db_host'):
            raise ValueError("Database host is required")

        port = data.get('db_port', 0)
        if not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535")

    def validate_api_key(self, data: dict):
        """Validate API key"""
        api_key = data.get('api_key')
        if not api_key:
            raise ValueError("API key is required")

        if len(api_key) < 16:
            raise ValueError("API key must be at least 16 characters")


# Raises ValueError if validation fails
config = ValidatedConfig("config.json").build()
```

### Runtime Overrides

```python
from rick.resource.config import JsonFileConfig


class AppConfig(JsonFileConfig):
    debug = False
    port = 8000
    host = "0.0.0.0"


# Load from file with runtime overrides
config = AppConfig("config.json").build(override_data={
    'debug': True,
    'port': 9000
})

print(config.debug)  # True (overridden)
print(config.port)  # 9000 (overridden)
print(config.host)  # Value from file or default
```

### Reload Configuration

```python
from rick.resource.config import JsonFileConfig


class ReloadableConfig(JsonFileConfig):
    setting1 = "default"
    setting2 = 42


config_loader = ReloadableConfig("config.json")
config = config_loader.build()

# Modify config.json...

# Reload from disk
config = config_loader.reload()
```

## TomlFileConfig

### Overview

`TomlFileConfig` loads configuration from TOML files. Requires Python 3.11+ (built-in `tomllib`) or the `tomli` package
for older versions.

### Installation

For Python < 3.11:

```bash
pip install tomli
```

### Basic Usage

```python
from rick.resource.config import TomlFileConfig


class AppConfig(TomlFileConfig):
    # Default values
    app_name = "MyApp"
    version = "1.0.0"
    debug = False

    # Nested structures are supported
    database = {}
    logging = {}


# Load from TOML file
config = AppConfig("config.toml").build()

print(config.app_name)  # Value from config.toml or default
print(config.database)  # Nested dict from TOML
```

### Example TOML File

**config.toml:**

```toml
app_name = "Production App"
version = "2.1.0"
debug = false

[database]
host = "db.example.com"
port = 5432
name = "production_db"
pool_size = 20

[logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
handlers = ["console", "file"]

[api]
base_url = "https://api.example.com"
timeout = 30
retry_attempts = 3

[[services]]
name = "auth"
url = "https://auth.example.com"
enabled = true

[[services]]
name = "billing"
url = "https://billing.example.com"
enabled = false
```

### With Validation

```python
from rick.resource.config import TomlFileConfig


class ValidatedTomlConfig(TomlFileConfig):
    app_name = "MyApp"
    database = {}
    logging = {}

    def validate_database(self, data: dict):
        """Validate database configuration"""
        db = data.get('database', {})

        if not db.get('host'):
            raise ValueError("Database host is required")

        port = db.get('port', 0)
        if not (1 <= port <= 65535):
            raise ValueError("Database port must be between 1 and 65535")

    def validate_logging(self, data: dict):
        """Validate logging configuration"""
        logging = data.get('logging', {})
        level = logging.get('level', 'INFO')

        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}")


config = ValidatedTomlConfig("config.toml").build()
```

## HybridFileConfig

### Overview

`HybridFileConfig` automatically detects the file format (JSON or TOML) based on the file extension and loads
accordingly.

### Supported Extensions

- `.json` - Loaded as JSON
- `.toml` - Loaded as TOML
- `.tml` - Loaded as TOML

### Basic Usage

```python
from rick.resource.config import HybridFileConfig


class FlexibleConfig(HybridFileConfig):
    debug = False
    port = 8000
    host = "localhost"

    def validate_port(self, data: dict):
        port = data.get('port', 0)
        if not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535")


# Works with either format
config1 = FlexibleConfig("config.json").build()
config2 = FlexibleConfig("config.toml").build()
config3 = FlexibleConfig("settings.tml").build()
```

### Use Case

Useful for applications that need to support multiple configuration formats:

```python
import sys
from rick.resource.config import HybridFileConfig


class AppConfig(HybridFileConfig):
    # Defaults
    app_name = "MyApp"
    debug = False
    port = 8000


# Load configuration from command line argument
config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"

try:
    config = AppConfig(config_file).build()
    print(f"Loaded configuration from {config_file}")
except Exception as e:
    print(f"Error loading config: {e}")
    sys.exit(1)
```

## Convenience Functions

Rick provides simple functions for quick configuration loading without defining classes:

### json_config_file()

Load JSON configuration file directly:

```python
from rick.resource.config import json_config_file

# Simple loading
config = json_config_file("config.json")

print(config.db_host)
print(config.api_key)
```

### toml_config_file()

Load TOML configuration file directly:

```python
from rick.resource.config import toml_config_file

# Simple loading
config = toml_config_file("config.toml")

print(config.app_name)
print(config.database)
```

### config_file()

Auto-detect and load configuration file:

```python
from rick.resource.config import config_file

# Auto-detect format based on extension
config = config_file("config.json")  # or config.toml

print(config.debug)
print(config.port)
```

### json_file() (Legacy)

Simple JSON file loader (legacy function):

```python
from rick.resource.config import json_file

# Basic JSON loading
config = json_file("config.json")
```

## Error Handling

### FileConfigError

All file configuration classes raise `FileConfigError` for configuration-related errors:

```python
from rick.resource.config import JsonFileConfig, FileConfigError


class MyConfig(JsonFileConfig):
    debug = False


try:
    config = MyConfig("nonexistent.json").build()
except FileConfigError as e:
    print(f"Configuration error: {e}")
    # Handle error: use defaults, exit, etc.
```

### Validation Errors

Validation functions should raise `ValueError` for validation failures:

```python
from rick.resource.config import EnvironmentConfig


class StrictConfig(EnvironmentConfig):
    API_KEY = None

    def validate_api_key(self, data: dict):
        if not data.get('api_key'):
            raise ValueError("API_KEY is required")


try:
    config = StrictConfig().build()
except ValueError as e:
    print(f"Validation failed: {e}")
```

## Best Practices

### 1. Use Validation for Critical Settings

```python
from rick.resource.config import JsonFileConfig


class ProductionConfig(JsonFileConfig):
    secret_key = None
    database_url = None

    def validate_production(self, data: dict):
        """Ensure production-critical settings are present"""
        if not data.get('secret_key'):
            raise ValueError("SECRET_KEY is required in production")

        if not data.get('database_url'):
            raise ValueError("DATABASE_URL is required in production")


config = ProductionConfig("production.json").build()
```

### 2. Provide Sensible Defaults

```python
from rick.resource.config import EnvironmentConfig


class AppConfig(EnvironmentConfig):
    # Good: sensible defaults for development
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    MAX_WORKERS = 4
    CACHE_TTL = 300

    # Override in production via environment variables
```

### 3. Use Type Hints via Default Values

```python
from rick.resource.config import EnvironmentConfig


class TypedConfig(EnvironmentConfig):
    # Type is inferred from default value
    PORT = 8000  # int
    DEBUG = False  # bool
    ALLOWED_HOSTS = []  # list
    DATABASE_CONFIG = {}  # dict
    API_KEY = None  # str (None defaults to str)
```

### 4. Separate Concerns with Multiple Configs

```python
from rick.resource.config import JsonFileConfig


class DatabaseConfig(JsonFileConfig):
    host = "localhost"
    port = 5432

    def validate_database(self, data):
        # Database-specific validation
        pass


class CacheConfig(JsonFileConfig):
    redis_host = "localhost"
    redis_port = 6379

    def validate_cache(self, data):
        # Cache-specific validation
        pass


# Load separate configs
db_config = DatabaseConfig("database.json").build()
cache_config = CacheConfig("cache.json").build()
```

### 5. Use StrOrFile for Secrets

```python
from rick.resource.config import EnvironmentConfig, StrOrFile


class SecureConfig(EnvironmentConfig):
    # Load from files in production, plain values in development
    DB_PASSWORD = StrOrFile(None)
    API_SECRET = StrOrFile(None)
    JWT_KEY = StrOrFile(None)


# Development: export DB_PASSWORD=dev_password
# Production: export DB_PASSWORD=/secrets/db-password

config = SecureConfig().build()
```

### 6. Environment-Specific Configuration

```python
import os
from rick.resource.config import JsonFileConfig


class AppConfig(JsonFileConfig):
    debug = False
    port = 8000


# Load config based on environment
env = os.getenv('APP_ENV', 'development')
config_files = {
    'development': 'config.dev.json',
    'staging': 'config.staging.json',
    'production': 'config.prod.json'
}

config_file = config_files.get(env, 'config.json')
config = AppConfig(config_file).build()
```

### 7. Combine Environment and File Configuration

```python
from rick.resource.config import EnvironmentConfig, JsonFileConfig


# Load base config from file
class BaseConfig(JsonFileConfig):
    app_name = "MyApp"
    port = 8000


file_config = BaseConfig("config.json").build()


# Override with environment variables
class EnvConfig(EnvironmentConfig):
    APP_NAME = file_config.app_name
    PORT = file_config.port
    DEBUG = False  # Override in env


final_config = EnvConfig().build()
```

## Complete Example

```python
import os
import sys
from rick.resource.config import HybridFileConfig, EnvironmentConfig, StrOrFile


class ApplicationConfig(HybridFileConfig):
    """File-based configuration with defaults"""

    # Application settings
    app_name = "MyApplication"
    version = "1.0.0"
    debug = False

    # Server settings
    host = "0.0.0.0"
    port = 8000
    workers = 4

    # Database settings
    database = {
        "host": "localhost",
        "port": 5432,
        "name": "myapp",
        "pool_size": 10
    }

    # Cache settings
    cache = {
        "enabled": True,
        "backend": "redis",
        "ttl": 300
    }

    # Validation
    def validate_server(self, data: dict):
        port = data.get('port', 0)
        if not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535")

        workers = data.get('workers', 0)
        if workers <= 0:
            raise ValueError("Workers must be positive")

    def validate_database(self, data: dict):
        db = data.get('database', {})
        if not db.get('host'):
            raise ValueError("Database host is required")


class RuntimeConfig(EnvironmentConfig):
    """Environment-based runtime overrides"""

    # Sensitive values loaded from environment
    SECRET_KEY = StrOrFile(None)
    DATABASE_PASSWORD = StrOrFile(None)
    API_KEY = StrOrFile(None)

    # Runtime overrides
    DEBUG = False
    PORT = 8000
    WORKERS = 4

    def validate_secrets(self, data: dict):
        if not data.get('secret_key'):
            raise ValueError("SECRET_KEY is required")

        if len(data.get('secret_key', '')) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")


def load_configuration():
    """Load application configuration"""

    # Determine config file
    env = os.getenv('APP_ENV', 'development')
    config_file = f"config.{env}.json"  # or .toml

    try:
        # Load base configuration from file
        file_config = ApplicationConfig(config_file).build()

        # Load runtime configuration from environment
        runtime_config = RuntimeConfig().build()

        # Merge configurations
        final_config = file_config.asdict()
        final_config.update(runtime_config.asdict())

        from rick.base import ShallowContainer
        return ShallowContainer(final_config)

    except Exception as e:
        print(f"Failed to load configuration: {e}", file=sys.stderr)
        sys.exit(1)


# Use in application
if __name__ == "__main__":
    config = load_configuration()

    print(f"Starting {config.app_name} v{config.version}")
    print(f"Server: {config.host}:{config.port}")
    print(f"Workers: {config.workers}")
    print(f"Debug: {config.debug}")
    print(f"Database: {config.database['host']}:{config.database['port']}")
```

## Related Topics

- [Redis Cache](redis.md) - Use configuration to set up Redis caching
- [Serializers](../serializers/index.md) - JSON serialization used in config files
- [Validators](../validators/index.md) - Validation patterns similar to config validation
