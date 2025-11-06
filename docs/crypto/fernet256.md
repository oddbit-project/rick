# Fernet256

Fernet256 provides symmetric encryption using AES-256-CBC with HMAC-SHA256 authentication. It is based on the Fernet
specification but uses 256-bit keys instead of 128-bit.

## Overview

Fernet256 offers authenticated encryption with the following features:

- **AES-256-CBC** encryption for data confidentiality
- **HMAC-SHA256** for data integrity and authentication
- **Timestamp verification** to detect token age
- **TTL support** for automatic expiration
- **URL-safe encoding** for easy storage and transport

## Basic Usage

### Generating Keys

```python
from rick.crypto import Fernet256

# Generate a new encryption key
key = Fernet256.generate_key()
# Returns: base64-encoded 64-byte key

# Save for later use
print(key.decode('utf-8'))
```

### Encrypting Data

```python
from rick.crypto import Fernet256

key = Fernet256.generate_key()
cipher = Fernet256(key)

# Encrypt data (must be bytes)
plaintext = b"Secret message"
token = cipher.encrypt(plaintext)

print(token)  # base64-encoded encrypted token
```

### Decrypting Data

```python
from rick.crypto import Fernet256

# Using the same key from encryption
cipher = Fernet256(key)

# Decrypt token
decrypted = cipher.decrypt(token)

assert decrypted == b"Secret message"
```

## API Reference

### Fernet256 Class

#### `__init__(key, backend=None)`

Initialize a Fernet256 cipher with the given key.

**Parameters:**

- `key` (bytes): Base64-encoded 64-byte encryption key
- `backend` (optional): Cryptography backend (uses default if not specified)

**Raises:**

- `ValueError`: If key is not exactly 64 bytes after base64 decoding

**Example:**

```python
from rick.crypto import Fernet256

key = Fernet256.generate_key()
cipher = Fernet256(key)
```

#### `generate_key()` (classmethod)

Generate a new random Fernet256 key.

**Returns:**

- `bytes`: Base64-encoded 64-byte key suitable for Fernet256

**Example:**

```python
key = Fernet256.generate_key()
# Save this key securely!
```

#### `encrypt(data)`

Encrypt data and return a Fernet token.

**Parameters:**

- `data` (bytes): Plaintext data to encrypt

**Returns:**

- `bytes`: Base64-encoded Fernet token

**Raises:**

- `TypeError`: If data is not bytes

**Example:**

```python
token = cipher.encrypt(b"secret data")
```

#### `decrypt(token, ttl=None)`

Decrypt a Fernet token.

**Parameters:**

- `token` (bytes): Encrypted Fernet token
- `ttl` (int, optional): Time-to-live in seconds. If set, token must be younger than TTL

**Returns:**

- `bytes`: Decrypted plaintext

**Raises:**

- `InvalidToken`: If token is invalid, tampered with, or expired

**Example:**

```python
# Decrypt without TTL
plaintext = cipher.decrypt(token)

# Decrypt with 1-hour TTL
plaintext = cipher.decrypt(token, ttl=3600)
```

#### `extract_timestamp(token)`

Extract the timestamp from a token without decrypting.

**Parameters:**

- `token` (bytes): Fernet token

**Returns:**

- `int`: Unix timestamp when token was created

**Raises:**

- `InvalidToken`: If token is invalid or tampered with

**Example:**

```python
import time

timestamp = cipher.extract_timestamp(token)
age = int(time.time()) - timestamp
print(f"Token is {age} seconds old")
```

#### `encrypt_at_time(data, current_time)`

Encrypt data with a specific timestamp (for testing).

**Parameters:**

- `data` (bytes): Plaintext data
- `current_time` (int): Unix timestamp to use

**Returns:**

- `bytes`: Base64-encoded Fernet token

#### `decrypt_at_time(token, ttl, current_time)`

Decrypt a token at a specific time (for testing).

**Parameters:**

- `token` (bytes): Encrypted token
- `ttl` (int): Time-to-live in seconds
- `current_time` (int): Unix timestamp to use for validation

**Returns:**

- `bytes`: Decrypted plaintext

**Raises:**

- `ValueError`: If ttl is None
- `InvalidToken`: If token is invalid or expired

## TTL (Time-To-Live)

TTL allows you to enforce token expiration:

```python
from rick.crypto import Fernet256
import time

cipher = Fernet256(Fernet256.generate_key())

# Encrypt data
data = b"expires soon"
token = cipher.encrypt(data)

# Decrypt immediately (works)
decrypted = cipher.decrypt(token, ttl=5)
print(decrypted)  # b"expires soon"

# Wait 6 seconds
time.sleep(6)

# Try to decrypt (fails)
try:
    cipher.decrypt(token, ttl=5)
except cipher.InvalidToken:
    print("Token expired!")
```

## String Encryption

Fernet256 works with bytes. For strings, encode/decode:

```python
from rick.crypto import Fernet256

cipher = Fernet256(Fernet256.generate_key())

# Encrypt string
text = "Hello, World!"
token = cipher.encrypt(text.encode('utf-8'))

# Decrypt to string
decrypted = cipher.decrypt(token).decode('utf-8')
assert decrypted == text
```

## Encrypting Complex Data

Use pickle or JSON for complex Python objects:

```python
from rick.crypto import Fernet256
import pickle
import json

cipher = Fernet256(Fernet256.generate_key())

# Using pickle
data = {'user': 'alice', 'roles': ['admin', 'user']}
token = cipher.encrypt(pickle.dumps(data))
decrypted = pickle.loads(cipher.decrypt(token))

# Using JSON
data = {'user': 'bob', 'age': 30}
token = cipher.encrypt(json.dumps(data).encode('utf-8'))
decrypted = json.loads(cipher.decrypt(token).decode('utf-8'))
```

## Token Format

Fernet256 tokens are URL-safe base64-encoded and contain:

```
Version (1 byte) || Timestamp (8 bytes) || IV (16 bytes) || Ciphertext (variable) || HMAC (32 bytes)
```

- **Version**: 0x81 (identifies Fernet256)
- **Timestamp**: Unix timestamp (8 bytes, big-endian)
- **IV**: Random initialization vector (16 bytes)
- **Ciphertext**: AES-256-CBC encrypted data
- **HMAC**: HMAC-SHA256 signature (32 bytes)

## MultiFernet256

MultiFernet256 supports multiple encryption keys for key rotation without downtime.

### Basic Usage

```python
from rick.crypto import Fernet256, MultiFernet256

# Create multiple keys
key1 = Fernet256.generate_key()
key2 = Fernet256.generate_key()

# Create multi-fernet (first key is primary)
multi = MultiFernet256([
    Fernet256(key1),  # Primary key for encryption
    Fernet256(key2),  # Secondary key for decryption
])

# Encryption uses primary key
token = multi.encrypt(b"data")

# Decryption tries all keys
decrypted = multi.decrypt(token)
```

### Key Rotation

```python
from rick.crypto import Fernet256, MultiFernet256

# Current production key
key_current = Fernet256.generate_key()

# New key for rotation
key_new = Fernet256.generate_key()

# Create multi-fernet with new key first
multi = MultiFernet256([
    Fernet256(key_new),  # New key (encrypts)
    Fernet256(key_current),  # Old key (decrypts)
])

# Old tokens encrypted with key_current
old_token = b"encrypted_with_old_key..."

# Rotate to new key
new_token = multi.rotate(old_token)

# New token is now encrypted with key_new
# but has the same timestamp as old_token
```

### MultiFernet256 API

#### `__init__(fernets)`

Create a MultiFernet256 instance.

**Parameters:**

- `fernets` (list): List of Fernet256 instances

**Raises:**

- `ValueError`: If fernets list is empty

#### `encrypt(msg)`

Encrypt using the first (primary) Fernet instance.

**Parameters:**

- `msg` (bytes): Data to encrypt

**Returns:**

- `bytes`: Encrypted token

#### `decrypt(msg, ttl=None)`

Decrypt using any Fernet instance.

**Parameters:**

- `msg` (bytes): Token to decrypt
- `ttl` (int, optional): Time-to-live in seconds

**Returns:**

- `bytes`: Decrypted data

**Raises:**

- `InvalidToken`: If no key can decrypt the token

#### `rotate(msg)`

Re-encrypt a token with the primary key.

**Parameters:**

- `msg` (bytes): Token encrypted with any key

**Returns:**

- `bytes`: Token encrypted with primary key (preserves timestamp)

**Raises:**

- `InvalidToken`: If token cannot be decrypted

## Use Cases

### Encrypted Configuration

```python
from rick.crypto import Fernet256
import json


class EncryptedConfig:
    def __init__(self, key):
        self.cipher = Fernet256(key)

    def save(self, config, filename):
        encrypted = self.cipher.encrypt(
            json.dumps(config).encode('utf-8')
        )
        with open(filename, 'wb') as f:
            f.write(encrypted)

    def load(self, filename):
        with open(filename, 'rb') as f:
            encrypted = f.read()
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode('utf-8'))
```

### Secure Session Tokens

```python
from rick.crypto import Fernet256
import pickle
import time


class SessionManager:
    def __init__(self, secret_key):
        self.cipher = Fernet256(secret_key)
        self.ttl = 3600  # 1 hour

    def create_token(self, user_id, data):
        session = {
            'user_id': user_id,
            'created': int(time.time()),
            'data': data
        }
        return self.cipher.encrypt(pickle.dumps(session))

    def verify_token(self, token):
        try:
            session = pickle.loads(
                self.cipher.decrypt(token, ttl=self.ttl)
            )
            return session
        except Fernet256.InvalidToken:
            return None
```

### Encrypted Database Fields

```python
from rick.crypto import Fernet256


class EncryptedField:
    def __init__(self, key):
        self.cipher = Fernet256(key)

    def encrypt(self, value):
        if value is None:
            return None
        return self.cipher.encrypt(
            value.encode('utf-8')
        ).decode('ascii')

    def decrypt(self, encrypted):
        if encrypted is None:
            return None
        return self.cipher.decrypt(
            encrypted.encode('ascii')
        ).decode('utf-8')


# Usage
field = EncryptedField(Fernet256.generate_key())

# Store in database
encrypted_ssn = field.encrypt("123-45-6789")

# Retrieve from database
ssn = field.decrypt(encrypted_ssn)
```

## Security Considerations

### Key Management

- **Never hard-code keys** in source code
- **Store keys securely** in environment variables or key vaults
- **Rotate keys regularly** using MultiFernet256
- **Use different keys** for different purposes/environments

### Best Practices

- **Always use TTL** for session tokens and temporary data
- **Re-encrypt periodically** to refresh timestamps
- **Validate tokens** before using decrypted data
- **Use secure random** for key generation (provided by `generate_key()`)

### Limitations

- **Not for large files** - Entire payload is loaded into memory
- **No compression** - Compress data before encryption if needed
- **Fixed algorithm** - Cannot change cipher without re-encrypting

## Error Handling

```python
from rick.crypto import Fernet256, InvalidToken

cipher = Fernet256(Fernet256.generate_key())

try:
    # Attempt decryption
    data = cipher.decrypt(token, ttl=3600)
except InvalidToken:
    # Token is invalid, tampered, or expired
    print("Invalid or expired token")
except ValueError as e:
    # Invalid parameters
    print(f"Configuration error: {e}")
except TypeError as e:
    # Wrong data type
    print(f"Type error: {e}")
```

## Performance

Fernet256 is suitable for small to medium-sized data:

- **Encryption**: ~1-5 ms for 1KB data
- **Decryption**: ~1-5 ms for 1KB data
- **Memory**: Entire payload in memory

For large files, consider:

- Streaming encryption (not supported by Fernet256)
- Hybrid encryption (encrypt symmetric key with Fernet256)
- Chunked encryption

## Related

- **[MultiFernet256](#multifernet256)** - Multi-key encryption
- **[CryptRedisCache](../resources/redis.md#cryptrediscache)** - Uses Fernet256 internally
- **[Buffer Hashing](buffer.md)** - Hash utilities
