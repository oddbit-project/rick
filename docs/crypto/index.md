# Cryptography

Rick provides cryptographic utilities for encryption, hashing, and password management. The crypto module offers secure
implementations for common cryptographic operations without the complexity of using cryptography libraries directly.

## Overview

The crypto module includes:

- **Fernet256** - Symmetric encryption using AES-256 with HMAC authentication
- **MultiFernet256** - Multi-key encryption support for key rotation
- **BcryptHasher** - Secure password hashing with bcrypt
- **Buffer Hashing** - SHA-1, SHA-256, SHA-512, and BLAKE2 hash utilities

## Components

### Encryption

Rick provides Fernet256, a 256-bit encryption implementation based on the Fernet specification:

- **[Fernet256](fernet256.md)** - Symmetric encryption with AES-256-CBC
- **[MultiFernet256](fernet256.md#multifernet256)** - Multi-key support for key rotation
- Authenticated encryption (encrypt-then-MAC)
- Built-in timestamp verification
- TTL (time-to-live) support

### Password Hashing

Secure password hashing using bcrypt:

- **[BcryptHasher](bcrypt.md)** - Password hashing and verification
- Configurable rounds (work factor)
- Automatic salt generation
- Constant-time comparison
- Rehash detection for security upgrades

### Hash Utilities

Buffer hashing utilities for files and streams:

- **[Buffer Hashing](buffer.md)** - SHA-1, SHA-256, SHA-512, BLAKE2
- Stream-based hashing
- Support for BytesIO objects
- Hexadecimal digest output

## Quick Examples

### Encryption with Fernet256

```python
from rick.crypto import Fernet256

# Generate a key
key = Fernet256.generate_key()

# Create cipher
cipher = Fernet256(key)

# Encrypt data
plaintext = b"Secret message"
token = cipher.encrypt(plaintext)

# Decrypt data
decrypted = cipher.decrypt(token)
assert decrypted == plaintext
```

### Password Hashing with Bcrypt

```python
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)

# Hash a password
password = "user_password_123"
pw_hash = hasher.hash(password)

# Verify password
is_valid = hasher.is_valid(password, pw_hash)
assert is_valid is True

# Check if rehash needed (for security upgrades)
if hasher.need_rehash(pw_hash):
    new_hash = hasher.hash(password)
```

### Buffer Hashing

```python
from rick.crypto import sha256_hash, sha512_hash
from io import BytesIO

data = BytesIO(b"Data to hash")

# SHA-256
hash_256 = sha256_hash(data)

# SHA-512
hash_512 = sha512_hash(data)
```

## Use Cases

### Secure Data Storage

```python
from rick.crypto import Fernet256
from rick.resource.redis import CryptRedisCache

# Use Fernet256 with encrypted Redis cache
key = Fernet256.generate_key()
cache = CryptRedisCache(
    key=key.decode('utf-8'),
    host='localhost'
)

# Store sensitive data
cache.set('api_token', {'token': 'secret_key_123'})
```

### Password Management

```python
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)


# User registration
def register_user(username, password):
    pw_hash = hasher.hash(password)
    # Store username and pw_hash in database
    return pw_hash


# User login
def login_user(username, password, stored_hash):
    if hasher.is_valid(password, stored_hash):
        # Check if hash needs upgrade
        if hasher.need_rehash(stored_hash):
            new_hash = hasher.hash(password)
            # Update database with new_hash
        return True
    return False
```

### File Integrity Verification

```python
from rick.crypto import sha256_hash
from io import BytesIO


def verify_file(file_path, expected_hash):
    with open(file_path, 'rb') as f:
        buffer = BytesIO(f.read())
        computed_hash = sha256_hash(buffer)
        return computed_hash == expected_hash
```

## Security Considerations

### Encryption

- **Key Management**: Store encryption keys securely (environment variables, key vaults)
- **Key Rotation**: Use MultiFernet256 for zero-downtime key rotation
- **TTL**: Set appropriate TTL values for time-sensitive data
- **Transport**: Always use encrypted transport (TLS) in addition to encryption at rest

### Password Hashing

- **Rounds**: Use at least 12 rounds for bcrypt (default)
- **Rehashing**: Regularly check and upgrade hashes as computational power increases
- **Timing**: The implementation uses constant-time comparison to prevent timing attacks
- **No Plain Text**: Never log or store passwords in plain text

### Hash Functions

- **SHA-1**: Considered weak for cryptographic purposes, use SHA-256 or higher
- **SHA-256**: Suitable for general cryptographic hashing
- **SHA-512**: Recommended for high-security applications
- **BLAKE2**: Modern, fast alternative to SHA-2 family

## Best Practices

### Key Generation

```python
from rick.crypto import Fernet256

# Generate key securely
key = Fernet256.generate_key()

# Store in environment variable or key vault
# NEVER hard-code keys in source code
import os

os.environ['ENCRYPTION_KEY'] = key.decode('utf-8')
```

### Password Policy

```python
from rick.crypto import BcryptHasher


class PasswordPolicy:
    def __init__(self):
        # Higher rounds = more secure but slower
        # Adjust based on your security requirements
        self.hasher = BcryptHasher(rounds=12)

    def is_strong(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True

    def hash_password(self, password):
        if not self.is_strong(password):
            raise ValueError("Password does not meet requirements")
        return self.hasher.hash(password)
```

### Key Rotation with MultiFernet

```python
from rick.crypto import Fernet256, MultiFernet256

# Current key
key_new = Fernet256.generate_key()

# Previous key (for decryption)
key_old = b'old_key_here...'

# Create multi-fernet with both keys
cipher = MultiFernet256([
    Fernet256(key_new),  # Primary key (for encryption)
    Fernet256(key_old),  # Old key (for decryption only)
])

# Decrypt with either key, encrypt with new key
token = cipher.encrypt(b"data")

# Rotate old encrypted data to new key
old_token = b"encrypted_with_old_key"
new_token = cipher.rotate(old_token)
```

## Documentation Sections

- **[Fernet256](fernet256.md)** - Symmetric encryption documentation
- **[BcryptHasher](bcrypt.md)** - Password hashing documentation
- **[Buffer Hashing](buffer.md)** - Hash utilities documentation

## Related Components

- **[CryptRedisCache](../resources/redis.md#cryptrediscache)** - Encrypted Redis cache using Fernet256
- **[EnvironmentConfig](../resources/config.md)** - Secure configuration with StrOrFile

## External Dependencies

The crypto module relies on:

- **cryptography** - Low-level cryptographic primitives
- **bcrypt** - Password hashing library

These are automatically installed when you install Rick.

## Standards Compliance

- **Fernet256**: Based on Fernet specification with 256-bit keys
- **Bcrypt**: Standard bcrypt algorithm with configurable work factor
- **SHA**: NIST standard hash functions (SHA-1, SHA-256, SHA-512)
- **BLAKE2**: RFC 7693 compliant
