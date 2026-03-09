# Changelog

All notable changes to the [Rick](https://github.com/oddbit-project/rick) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.8.1]

### Added
- Event manager documentation and examples (basic events, class handlers, priority handlers, state serialization)
- Test coverage for crypto, event, and file documentation modules

### Fixed
- Misc bugfixes across multiple modules (container, DI, maploader, event manager, filter, request record, environment config, file config, redis, multipart reader, cast utilities, validator)
- Documentation link fixes
- Test badge fix

## [0.8.0] - 2025-11-06

### Added
- MessagePack serializer with bidirectional encoding/decoding
- RedisCache improvements: custom serializer/deserializer support, key prefix support, `get()` hit ratio statistics
- Fernet256 additional tests
- Experimental SBOM (Software Bill of Materials) support
- Crypto examples and documentation
- Validator examples
- Form documentation updates

### Changed
- Dropped Python 3.8 support; added Python 3.13 and 3.14 support
- Migrated repository from git.oddbit.org to GitHub
- Documentation switched to dark theme
- Updated setup/tox configuration

### Fixed
- RedisCache prefix bugfix
- Security: updated requirements.txt to reduce vulnerabilities

## [0.7.1] - 2025-07-30

### Added
- Optional `backend` parameter in `RedisCache` constructor to wrap existing Redis client instances
- Unit test and documentation updates

## [0.7.0] - 2024-08-13

### Fixed
- Bugfix release
- GitHub Actions updates
- Pinned `requests` to avoid compatibility issues with tox-docker
- tox-docker Redis adjustments

## [0.6.9] - 2024-08-13

### Added
- `int` and `idlist` validators with unit tests
- `seek()` support for `MultiPartReader`

### Changed
- Redis dependency update; tox-docker updates

### Fixed
- README.md formatting fix

## [0.6.7] - 2024-01-08

### Changed
- **BREAKING**: `RedisCache.has()` now returns `bool` instead of integer

### Added
- Redis unit tests

## [0.6.6] - 2023-12-20

### Added
- Support for `bytes` and `memoryview` types in `ExtendedJsonEncoder`

### Fixed
- Test fix

## [0.6.5] - 2023-12-14

### Fixed
- `MapLoader.register()` bugfix

## [0.6.4] - 2023-12-14

### Added
- `MapLoader.register()` method

## [0.6.3] - 2023-11-15

### Added
- BytesIO BLAKE2 hash helper
- Package include improvements

### Fixed
- Boolean values were not parsed correctly from environment variables in `EnvironmentConfig`
- Updated GitHub Action

## [0.6.2] - 2023-10-03

### Added
- `CamelCaseJsonSerializer` for automatic camelCase JSON encoding

## [0.6.1] - 2023-05-31

Version bump release.

## [0.6.0] - 2023-05-31

### Added
- GitHub Actions CI setup
- `FileReader` implementation with custom attribute support
- `bytesioslice` utility (renamed from `byteslice`)
- Optional exception raising in `load_class()`
- `ClassRegistry` implementation
- `MultiPartReader` for multipart/form-data stream processing
- `list_duplicates()` utility function
- MapLoader cached item cleaning

### Changed
- **BREAKING**: Removed `optional()` function
- `EventManager`: non-existing events are now silently ignored; `dispatch()` returns `bool` indicating if dispatch occurred
- Dependency version updates
- Code formatting improvements
- Documentation URL updates

### Fixed
- `FileReader`: removal of problematic attributes
- Unit test fixes

## [0.4.6] - 2022-11-25

### Added
- `ClassRegistry` implementation

## [0.4.5] - 2022-11-17

### Added
- `RequestRecord` for form-like request validation
- `ConsoleWriter` and `AnsiColor` for terminal output
- `EnvironmentConfig` with docker-style secrets file support
- `Container`-based environment configuration
- DateTime helper utilities
- JSON serializer (`ExtendedJsonEncoder`)
- Form filters and custom validation
- Form builder with controls, fieldsets, and readonly support
- `Runnable` mixin
- String-case utility functions

### Changed
- **BREAKING**: `RequestRecord.get_object()` renamed to `RequestRecord.bind()`; `bind()` only binds non-None attribute values
- **BREAKING**: `field.messages` renamed to `field.error_message`; custom error message is now a string per field instead of a dict
- **BREAKING**: `form.fieldrecord` renamed to `form.requestrecord`
- Removed Injectable/DI from Event Manager

### Fixed
- JSON exception trapping for reliability
- Redis serializer fix
- Various unit test fixes

## [0.4.0] - Initial releases

### Added
- Core dependency injection container (`Di`) with singleton and factory patterns
- Base containers (`Container`, `MutableContainer`, `ShallowContainer`)
- `Registry` class for dynamic class registration
- `MapLoader` for configuration loading
- Redis cache support (`RedisCache`)
- Fernet256 encryption
- BCrypt password hashing (`BcryptHasher`)
- Buffer hashing (SHA1, SHA256, SHA512, BLAKE2)
- Event manager with priority-based dispatch
- Translation mixin
- Injectable mixin
- Validator framework with string, numeric, network, hash, and misc validators

[Unreleased]: https://github.com/oddbit-project/rick/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/oddbit-project/rick/compare/0.7.1...v0.8.0
[0.7.1]: https://github.com/oddbit-project/rick/compare/0.7.0...0.7.1
[0.7.0]: https://github.com/oddbit-project/rick/compare/0.6.9...0.7.0
[0.6.9]: https://github.com/oddbit-project/rick/compare/0.6.7...0.6.9
[0.6.7]: https://github.com/oddbit-project/rick/compare/0.6.6...0.6.7
[0.6.6]: https://github.com/oddbit-project/rick/compare/0.6.5...0.6.6
[0.6.5]: https://github.com/oddbit-project/rick/compare/0.6.4...0.6.5
[0.6.4]: https://github.com/oddbit-project/rick/compare/0.6.3...0.6.4
[0.6.3]: https://github.com/oddbit-project/rick/compare/0.6.2...0.6.3
[0.6.2]: https://github.com/oddbit-project/rick/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/oddbit-project/rick/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/oddbit-project/rick/compare/0.4.6...0.6.0
[0.4.6]: https://github.com/oddbit-project/rick/compare/0.4.5...0.4.6
[0.4.5]: https://github.com/oddbit-project/rick/releases/tag/0.4.5
