# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.8.0]

### Added
- **Serializers**: New MessagePack serializer with bidirectional encoding/decoding
  - Full support for datetime, Decimal, UUID, dataclasses, and custom objects
  - 30-50% smaller than JSON, 2-4x faster serialization
  - Custom extension types for Python-specific objects

### Documentation
- **Comprehensive Documentation**: Complete documentation for all components
  - Serializers documentation (JSON and MessagePack)
  - Configuration management documentation (Environment, JSON, TOML, Hybrid)
  - Redis Cache documentation with examples
  - Console Output documentation (AnsiColor and ConsoleWriter)
  - Resource management documentation
- **Improved README**: Enhanced with complete feature overview and examples
- **Improved Index**: Comprehensive library overview with architecture patterns
- **Code Examples**: Added practical examples throughout documentation

## [v0.7.1] - 2025-07-30

### Added
- **Redis Cache**: Optional `backend` parameter in `RedisCache` constructor to wrap existing Redis client instances
- **Dependencies**: Updated cryptography to >=45.0.5
- **Dependencies**: Updated bcrypt to >=4.3.0
- **Dependencies**: Updated setuptools to >=73.0.1
- **Dependencies**: Updated wheel to 0.44.0

### Fixed
- **Stream Processing**: Fixed MultiPartReader stream handling edge cases
- **Constants**: Corrected version string formatting
- **Configuration**: Improved error handling in environment configuration loading

### Security
- **Cache**: Enhanced encryption support in `CryptRedisCache`
- **Validation**: Strengthened input validation across all validators
- **Dependencies**: Updated all security-critical dependencies to latest versions

### Development
- **CI/CD**: Updated GitHub Actions for better test coverage
- **Testing**: Added comprehensive unit tests for new validators
- **Testing**: Enhanced Redis cache testing with encrypted cache scenarios
- **Documentation**: Updated validator documentation with new validators

### Internal
- **Refactoring**: Improved code organization in validator rules
- **Refactoring**: Enhanced error handling consistency across modules
- **Performance**: Optimized stream processing operations
- **Type Safety**: Enhanced type hints across validator modules


## Links
- [Repository](https://github.com/oddbit-project/rick)
- [Documentation](https://docs.oddbit.org/rick/)
- [Security Policy](SECURITY.md)