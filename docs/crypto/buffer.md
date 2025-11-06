# Buffer Hashing

Buffer hashing utilities provide convenient functions for computing cryptographic hashes of data streams. These
utilities are designed for hashing BytesIO objects, making them ideal for file integrity verification, data validation,
and content addressing.

## Overview

Rick provides hash utilities for the most common cryptographic hash functions:

- **SHA-256** - Industry standard for general-purpose hashing
- **SHA-512** - Higher security variant of SHA-2
- **SHA-1** - Legacy support (not recommended for security)
- **BLAKE2** - Modern, fast alternative to SHA-2

All hash functions work with `BytesIO` objects and return hexadecimal digest strings.

## Basic Usage

### SHA-256 Hash

```python
from rick.crypto import sha256_hash
from io import BytesIO

# Hash some data
data = BytesIO(b"Hello, World!")
hash_value = sha256_hash(data)

print(hash_value)
# Output: dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f
```

### SHA-512 Hash

```python
from rick.crypto import sha512_hash
from io import BytesIO

data = BytesIO(b"Hello, World!")
hash_value = sha512_hash(data)

print(hash_value)
# Output: 374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6c...
```

### SHA-1 Hash

```python
from rick.crypto import sha1_hash
from io import BytesIO

data = BytesIO(b"Hello, World!")
hash_value = sha1_hash(data)

print(hash_value)
# Output: 0a0a9f2a6772942557ab5355d76af442f8f65e01
```

### BLAKE2 Hash

```python
from rick.crypto import blake2_hash
from io import BytesIO

data = BytesIO(b"Hello, World!")
hash_value = blake2_hash(data)

print(hash_value)
# Output: 021ced8799296ceca557832ab941a50b4a11f83478cf141f51f933f653ab9fbc...
```

## API Reference

### `sha256_hash(buf)`

Compute SHA-256 hash of a buffer.

**Parameters:**

- `buf` (BytesIO): Buffer containing data to hash

**Returns:**

- `str`: Hexadecimal digest string (64 characters)

**Example:**

```python
from rick.crypto import sha256_hash
from io import BytesIO

data = BytesIO(b"data to hash")
digest = sha256_hash(data)
```

**Note:** The function automatically seeks to the beginning of the buffer before reading.

### `sha512_hash(buf)`

Compute SHA-512 hash of a buffer.

**Parameters:**

- `buf` (BytesIO): Buffer containing data to hash

**Returns:**

- `str`: Hexadecimal digest string (128 characters)

**Example:**

```python
from rick.crypto import sha512_hash
from io import BytesIO

data = BytesIO(b"data to hash")
digest = sha512_hash(data)
```

### `sha1_hash(buf)`

Compute SHA-1 hash of a buffer.

**Parameters:**

- `buf` (BytesIO): Buffer containing data to hash

**Returns:**

- `str`: Hexadecimal digest string (40 characters)

**Example:**

```python
from rick.crypto import sha1_hash
from io import BytesIO

data = BytesIO(b"data to hash")
digest = sha1_hash(data)
```

**Security Warning:** SHA-1 is considered cryptographically broken and should not be used for security purposes. Use
SHA-256 or higher instead.

### `blake2_hash(buf)`

Compute BLAKE2b hash of a buffer.

**Parameters:**

- `buf` (BytesIO): Buffer containing data to hash

**Returns:**

- `str`: Hexadecimal digest string (128 characters)

**Example:**

```python
from rick.crypto import blake2_hash
from io import BytesIO

data = BytesIO(b"data to hash")
digest = blake2_hash(data)
```

**Note:** BLAKE2b is faster than SHA-2 and provides excellent security properties.

### `hash_buffer(method, buf)`

Generic hash function that supports any hashlib algorithm.

**Parameters:**

- `method` (str): Name of the hash algorithm (e.g., "sha256", "md5", "sha384")
- `buf` (BytesIO): Buffer containing data to hash

**Returns:**

- `str`: Hexadecimal digest string

**Raises:**

- `RuntimeError`: If the specified method is not available in hashlib

**Example:**

```python
from rick.crypto.buffer import hash_buffer
from io import BytesIO

data = BytesIO(b"data to hash")

# Use SHA-256
sha256 = hash_buffer("sha256", data)

# Use SHA-384
sha384 = hash_buffer("sha384", data)

# Use MD5 (not recommended for security)
md5 = hash_buffer("md5", data)
```

## File Hashing

### Hashing Files

```python
from rick.crypto import sha256_hash
from io import BytesIO


def hash_file(file_path):
    """Compute SHA-256 hash of a file"""
    with open(file_path, 'rb') as f:
        data = BytesIO(f.read())
        return sha256_hash(data)


# Hash a file
file_hash = hash_file('/path/to/file.txt')
print(f"File hash: {file_hash}")
```

### Verifying File Integrity

```python
from rick.crypto import sha256_hash
from io import BytesIO


def verify_file(file_path, expected_hash):
    """Verify file integrity against expected hash"""
    with open(file_path, 'rb') as f:
        data = BytesIO(f.read())
        computed_hash = sha256_hash(data)
        return computed_hash == expected_hash


# Verify a file
is_valid = verify_file('/path/to/file.txt', 'expected_hash_here')
if is_valid:
    print("File integrity verified")
else:
    print("File has been modified or corrupted")
```

### Hashing Large Files

For large files, read in chunks to avoid memory issues:

```python
from rick.crypto import sha256_hash
from io import BytesIO
import hashlib


def hash_large_file(file_path, chunk_size=8192):
    """Hash large file by reading in chunks"""
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


# Hash large file
large_file_hash = hash_large_file('/path/to/large_file.bin')
```

## Content Addressing

### Creating Content-Addressable Storage

```python
from rick.crypto import sha256_hash
from io import BytesIO
import os


class ContentStore:
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def store(self, data):
        """Store data and return its hash"""
        buffer = BytesIO(data)
        content_hash = sha256_hash(buffer)

        # Store using hash as filename
        file_path = os.path.join(self.storage_dir, content_hash)
        with open(file_path, 'wb') as f:
            f.write(data)

        return content_hash

    def retrieve(self, content_hash):
        """Retrieve data by hash"""
        file_path = os.path.join(self.storage_dir, content_hash)
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'rb') as f:
            return f.read()


# Usage
store = ContentStore('/tmp/content_store')

# Store data
data = b"Important document content"
content_id = store.store(data)
print(f"Stored with ID: {content_id}")

# Retrieve data
retrieved = store.retrieve(content_id)
assert retrieved == data
```

## Data Validation

### Checksum Validation

```python
from rick.crypto import sha256_hash
from io import BytesIO


class DataValidator:
    @staticmethod
    def create_checksum(data):
        """Create checksum for data"""
        buffer = BytesIO(data)
        return sha256_hash(buffer)

    @staticmethod
    def validate(data, checksum):
        """Validate data against checksum"""
        computed = DataValidator.create_checksum(data)
        return computed == checksum


# Usage
validator = DataValidator()

# Create checksum
data = b"Important data"
checksum = validator.create_checksum(data)

# Later, validate the data
is_valid = validator.validate(data, checksum)
if is_valid:
    print("Data is intact")
else:
    print("Data has been corrupted")
```

### Download Verification

```python
from rick.crypto import sha256_hash
from io import BytesIO
import urllib.request


def download_and_verify(url, expected_hash):
    """Download file and verify its hash"""
    # Download file
    response = urllib.request.urlopen(url)
    content = response.read()

    # Compute hash
    buffer = BytesIO(content)
    computed_hash = sha256_hash(buffer)

    # Verify
    if computed_hash != expected_hash:
        raise ValueError(f"Hash mismatch! Expected {expected_hash}, got {computed_hash}")

    return content


# Download and verify
try:
    content = download_and_verify(
        'https://example.com/file.bin',
        'expected_sha256_hash_here'
    )
    print("Download verified successfully")
except ValueError as e:
    print(f"Verification failed: {e}")
```

## Duplicate Detection

### Detecting Duplicate Files

```python
from rick.crypto import sha256_hash
from io import BytesIO
import os


def find_duplicates(directory):
    """Find duplicate files by hash"""
    hashes = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Hash file
            with open(file_path, 'rb') as f:
                buffer = BytesIO(f.read())
                file_hash = sha256_hash(buffer)

            # Check for duplicates
            if file_hash in hashes:
                duplicates.append((file_path, hashes[file_hash]))
            else:
                hashes[file_hash] = file_path

    return duplicates


# Find duplicates
dupes = find_duplicates('/path/to/directory')
for dup1, dup2 in dupes:
    print(f"Duplicate found: {dup1} == {dup2}")
```

## Choosing a Hash Algorithm

### SHA-256

- **Best for**: General-purpose hashing, file integrity, data validation
- **Output size**: 256 bits (64 hex chars)
- **Speed**: Fast
- **Security**: High (recommended)

```python
from rick.crypto import sha256_hash
from io import BytesIO

data = BytesIO(b"data")
hash_value = sha256_hash(data)  # 64 characters
```

### SHA-512

- **Best for**: High-security applications, password derivation
- **Output size**: 512 bits (128 hex chars)
- **Speed**: Moderate
- **Security**: Very high

```python
from rick.crypto import sha512_hash
from io import BytesIO

data = BytesIO(b"data")
hash_value = sha512_hash(data)  # 128 characters
```

### BLAKE2

- **Best for**: High-performance applications, modern systems
- **Output size**: 512 bits (128 hex chars)
- **Speed**: Very fast (faster than SHA-2)
- **Security**: High

```python
from rick.crypto import blake2_hash
from io import BytesIO

data = BytesIO(b"data")
hash_value = blake2_hash(data)  # 128 characters
```

### SHA-1 (Legacy)

- **Best for**: Git commit IDs, legacy compatibility only
- **Output size**: 160 bits (40 hex chars)
- **Speed**: Fast
- **Security**: Broken (NOT recommended for security)

```python
from rick.crypto import sha1_hash
from io import BytesIO

data = BytesIO(b"data")
hash_value = sha1_hash(data)  # 40 characters
```

## Performance Comparison

```python
from rick.crypto import sha256_hash, sha512_hash, sha1_hash, blake2_hash
from io import BytesIO
import time

# Prepare test data (1 MB)
test_data = BytesIO(b"x" * (1024 * 1024))

# Benchmark each algorithm
algorithms = [
    ("SHA-1", sha1_hash),
    ("SHA-256", sha256_hash),
    ("SHA-512", sha512_hash),
    ("BLAKE2", blake2_hash),
]

for name, hash_func in algorithms:
    test_data.seek(0)
    start = time.time()
    hash_value = hash_func(test_data)
    elapsed = time.time() - start
    print(f"{name}: {elapsed * 1000:.2f}ms, digest: {hash_value[:16]}...")
```

## Common Use Cases

### Database Record Hashing

```python
from rick.crypto import sha256_hash
from io import BytesIO
import json


def hash_record(record):
    """Create hash of database record"""
    # Serialize to JSON (deterministic order)
    json_data = json.dumps(record, sort_keys=True)
    buffer = BytesIO(json_data.encode('utf-8'))
    return sha256_hash(buffer)


# Usage
record = {
    'id': 123,
    'name': 'Alice',
    'email': 'alice@example.com'
}

record_hash = hash_record(record)
print(f"Record hash: {record_hash}")
```

### API Response Validation

```python
from rick.crypto import sha256_hash
from io import BytesIO
import json


def validate_api_response(response_data, signature):
    """Validate API response hasn't been tampered with"""
    buffer = BytesIO(json.dumps(response_data, sort_keys=True).encode())
    computed_hash = sha256_hash(buffer)
    return computed_hash == signature


# Server side: create signature
response = {'status': 'success', 'data': [1, 2, 3]}
buffer = BytesIO(json.dumps(response, sort_keys=True).encode())
signature = sha256_hash(buffer)

# Client side: validate
is_valid = validate_api_response(response, signature)
```

### Caching with Hash Keys

```python
from rick.crypto import sha256_hash
from io import BytesIO
import json


class CacheManager:
    def __init__(self):
        self.cache = {}

    def generate_key(self, *args, **kwargs):
        """Generate cache key from function arguments"""
        data = {
            'args': args,
            'kwargs': kwargs
        }
        json_data = json.dumps(data, sort_keys=True)
        buffer = BytesIO(json_data.encode('utf-8'))
        return sha256_hash(buffer)

    def get(self, *args, **kwargs):
        key = self.generate_key(*args, **kwargs)
        return self.cache.get(key)

    def set(self, value, *args, **kwargs):
        key = self.generate_key(*args, **kwargs)
        self.cache[key] = value


# Usage
cache = CacheManager()

# Cache result
cache.set('result_data', user_id=123, action='fetch')

# Retrieve from cache
cached = cache.get(user_id=123, action='fetch')
```

## Security Considerations

### Hash Function Selection

- **SHA-256**: Recommended for general use
- **SHA-512**: Use for high-security applications
- **BLAKE2**: Good alternative to SHA-2, faster
- **SHA-1**: Avoid for security purposes (collisions found)

### Not for Passwords

Hash functions are NOT suitable for password hashing:

```python
# DON'T: Use hash functions for passwords
from rick.crypto import sha256_hash

password_hash = sha256_hash(BytesIO(password.encode()))  # INSECURE

# DO: Use BcryptHasher for passwords
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)
password_hash = hasher.hash(password)  # SECURE
```

### Timing Attacks

For comparing hashes, use constant-time comparison:

```python
import hmac


def safe_compare(hash1, hash2):
    """Compare hashes safely"""
    return hmac.compare_digest(hash1, hash2)


# DON'T: Direct comparison (timing attack vulnerability)
if computed_hash == stored_hash:
    pass

# DO: Constant-time comparison
if safe_compare(computed_hash, stored_hash):
    pass
```

## Error Handling

```python
from rick.crypto.buffer import hash_buffer
from io import BytesIO

try:
    # Invalid hash method
    hash_buffer("invalid_method", BytesIO(b"data"))
except RuntimeError as e:
    print(f"Invalid hash method: {e}")

# Ensure buffer is seekable
data = BytesIO(b"data")
try:
    hash_value = sha256_hash(data)
except Exception as e:
    print(f"Error hashing buffer: {e}")
```

## Related

- **[BcryptHasher](bcrypt.md)** - Password hashing (use for passwords, not these functions)
- **[Fernet256](fernet256.md)** - Symmetric encryption
- **[Redis Cache](../resources/redis.md)** - Uses hash functions internally

## Standards

- **SHA-256**: FIPS 180-4 compliant
- **SHA-512**: FIPS 180-4 compliant
- **SHA-1**: FIPS 180-1 (deprecated for cryptographic use)
- **BLAKE2**: RFC 7693 compliant
