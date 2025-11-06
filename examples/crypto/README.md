# Rick Crypto Examples

This directory contains practical examples demonstrating the Rick crypto module features.

## Examples Overview

### Fernet256 Encryption

#### `fernet256_basic.py`
Basic encryption and decryption examples:
- Key generation
- Encrypting and decrypting bytes
- String encryption
- Complex data encryption with JSON
- Time-to-live (TTL) tokens

**Run:**
```bash
python examples/crypto/fernet256_basic.py
```

#### `fernet256_key_rotation.py`
Key rotation with MultiFernet256:
- Using multiple encryption keys
- Zero-downtime key rotation
- Gradual migration strategies
- Multi-environment key management

**Run:**
```bash
python examples/crypto/fernet256_key_rotation.py
```

#### `fernet256_use_cases.py`
Practical use cases:
- Encrypted configuration files
- Session token management
- Encrypted database fields
- Secure API tokens

**Run:**
```bash
python examples/crypto/fernet256_use_cases.py
```

### Password Hashing

#### `bcrypt_basic.py`
Basic password hashing:
- Hashing and verifying passwords
- Different work factors (rounds)
- Rehash detection for upgrades
- Understanding hash format
- Password strength basics

**Run:**
```bash
python examples/crypto/bcrypt_basic.py
```

#### `bcrypt_authentication.py`
Complete authentication system:
- User registration and login
- Password policy enforcement
- Automatic hash upgrades
- Account lockout protection
- Password change functionality

**Run:**
```bash
python examples/crypto/bcrypt_authentication.py
```

### Buffer Hashing

#### `buffer_hashing.py`
Hash functions for data integrity:
- SHA-256, SHA-512, SHA-1, BLAKE2 usage
- File integrity verification
- Content-addressable storage
- Duplicate detection
- Data validation with checksums

**Run:**
```bash
python examples/crypto/buffer_hashing.py
```

## Quick Start

### Installation

First, ensure Rick is installed:
```bash
pip install rick
```

Or install from source:
```bash
cd /path/to/rick
pip install -e .
```

### Running Examples

Run any example directly:
```bash
python examples/crypto/fernet256_basic.py
```

Or run all examples:
```bash
for example in examples/crypto/*.py; do
    echo "Running $example..."
    python "$example"
    echo ""
done
```

## Example Categories

### Encryption (Fernet256)
- **Security**: AES-256-CBC encryption with HMAC-SHA256 authentication
- **Use cases**: Configuration files, session tokens, sensitive data storage
- **Features**: TTL support, key rotation, multi-key decryption

### Password Hashing (Bcrypt)
- **Security**: Industry-standard bcrypt with configurable work factor
- **Use cases**: User authentication, password storage
- **Features**: Automatic salt, rehash detection, timing-safe comparison

### Hashing (Buffer Utilities)
- **Algorithms**: SHA-256, SHA-512, SHA-1 (legacy), BLAKE2
- **Use cases**: File integrity, content addressing, checksums
- **Features**: Fast hashing, multiple algorithm support

## Common Patterns

### Secure Configuration Storage

```python
from rick.crypto import Fernet256
import json

key = Fernet256.generate_key()
cipher = Fernet256(key)

# Encrypt config
config = {'database': 'localhost', 'password': 'secret'}
encrypted = cipher.encrypt(json.dumps(config).encode('utf-8'))

# Decrypt config
decrypted = json.loads(cipher.decrypt(encrypted).decode('utf-8'))
```

### User Authentication

```python
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)

# Registration
password_hash = hasher.hash(user_password)
# Store password_hash in database

# Login
if hasher.is_valid(user_password, stored_hash):
    # Check for upgrade
    if hasher.need_rehash(stored_hash):
        new_hash = hasher.hash(user_password)
        # Update database
```

### File Integrity

```python
from rick.crypto import sha256_hash
from io import BytesIO

# Create checksum
with open('file.txt', 'rb') as f:
    checksum = sha256_hash(BytesIO(f.read()))

# Verify later
with open('file.txt', 'rb') as f:
    computed = sha256_hash(BytesIO(f.read()))
    is_valid = computed == checksum
```

## Security Best Practices

### Encryption
- **Never hardcode keys** - Use environment variables or key vaults
- **Rotate keys regularly** - Use MultiFernet256 for zero-downtime rotation
- **Use TTL appropriately** - Set expiration for time-sensitive tokens
- **Different keys for different purposes** - Don't reuse encryption keys

### Password Hashing
- **Use adequate rounds** - Minimum 12, increase as hardware improves
- **Never log passwords** - Only log authentication success/failure
- **Check for rehash** - Upgrade hashes when rounds increase
- **Implement rate limiting** - Prevent brute-force attacks

### Hashing
- **SHA-1 is deprecated** - Use SHA-256 or higher for security
- **Not for passwords** - Use BcryptHasher instead
- **Verify integrity** - Always validate checksums
- **Use constant-time comparison** - Prevent timing attacks

## Documentation

For complete documentation, see:
- [Crypto Overview](../../docs/crypto/index.md)
- [Fernet256](../../docs/crypto/fernet256.md)
- [BcryptHasher](../../docs/crypto/bcrypt.md)
- [Buffer Hashing](../../docs/crypto/buffer.md)

## Support

- **Issues**: https://github.com/oddbit-project/rick/issues
- **Documentation**: https://oddbit-project.github.io/rick/
- **Repository**: https://github.com/oddbit-project/rick
