# BcryptHasher

BcryptHasher provides secure password hashing using the bcrypt algorithm with configurable work factor (rounds). It
includes automatic salt generation, constant-time comparison, and rehash detection for security upgrades.

## Overview

Bcrypt is specifically designed for password hashing with these features:

- **Adaptive cost** - Configurable work factor that can increase as hardware improves
- **Automatic salt** - Random salt generated for each password
- **Slow by design** - Intentionally slow to resist brute-force attacks
- **Timing-safe comparison** - Prevents timing attacks during verification

## Basic Usage

### Hashing Passwords

```python
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)

# Hash a password
password = "user_password_123"
pw_hash = hasher.hash(password)

print(pw_hash)
# Output: $2b$12$randomsalt...hashedpassword
```

### Verifying Passwords

```python
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)

password = "user_password_123"
pw_hash = hasher.hash(password)

# Verify correct password
is_valid = hasher.is_valid(password, pw_hash)
print(is_valid)  # True

# Verify incorrect password
is_valid = hasher.is_valid("wrong_password", pw_hash)
print(is_valid)  # False
```

### Checking for Rehash

```python
from rick.crypto import BcryptHasher

# Current hasher with 14 rounds
hasher = BcryptHasher(rounds=14)

# Old hash created with 12 rounds
old_hash = "$2b$12$..."

# Check if rehash is needed
if hasher.need_rehash(old_hash):
    # Re-hash password with current rounds
    new_hash = hasher.hash(password)
    # Update database with new_hash
```

## API Reference

### BcryptHasher Class

#### `__init__(rounds=None, prefix=None)`

Initialize a BcryptHasher with specified configuration.

**Parameters:**

- `rounds` (int, optional): Number of bcrypt rounds (work factor). Default: 12
    - Valid range: 4-31
    - Each increment doubles the computation time
    - Recommended minimum: 12
- `prefix` (str, optional): Bcrypt prefix/version. Default: "2b"
    - "2a": Compatible with most systems
    - "2b": Current standard (recommended)
    - "2y": PHP compatibility

**Example:**

```python
# Default configuration (12 rounds, 2b prefix)
hasher = BcryptHasher()

# Custom configuration
hasher = BcryptHasher(rounds=14, prefix="2b")
```

#### `hash(password)`

Hash a password using bcrypt.

**Parameters:**

- `password` (str): Cleartext password to hash

**Returns:**

- `str`: Bcrypt hash string

**Raises:**

- `ValueError`: If password is empty

**Example:**

```python
pw_hash = hasher.hash("my_secure_password")
```

**Note:** The password is first hashed with SHA-256 before bcrypt to handle passwords longer than 72 bytes.

#### `is_valid(password, pw_hash)`

Verify a password against a hash.

**Parameters:**

- `password` (str): Cleartext password to verify
- `pw_hash` (str): Bcrypt hash to check against

**Returns:**

- `bool`: True if password matches hash, False otherwise

**Example:**

```python
if hasher.is_valid(user_password, stored_hash):
    print("Password correct")
else:
    print("Invalid password")
```

**Security:** Uses constant-time comparison to prevent timing attacks.

#### `need_rehash(pw_hash, prefix=None)`

Check if a hash needs to be rehashed with current configuration.

**Parameters:**

- `pw_hash` (str): Bcrypt hash to check
- `prefix` (str, optional): Expected prefix. Default: uses instance prefix

**Returns:**

- `bool`: True if hash uses fewer rounds than current configuration

**Raises:**

- `ValueError`: If hash is invalid or malformed

**Example:**

```python
hasher = BcryptHasher(rounds=14)

old_hash = "$2b$12$..."  # Created with 12 rounds

if hasher.need_rehash(old_hash):
    # Rounds increased from 12 to 14, should rehash
    new_hash = hasher.hash(password)
```

## Understanding Rounds (Work Factor)

The rounds parameter determines how computationally expensive the hashing is:

| Rounds | Time (approx) | Security Level      |
|--------|---------------|---------------------|
| 10     | ~70ms         | Minimum acceptable  |
| 12     | ~280ms        | Recommended default |
| 14     | ~1.1s         | High security       |
| 16     | ~4.5s         | Very high security  |

```python
import time
from rick.crypto import BcryptHasher

# Test different round values
for rounds in [10, 12, 14]:
    hasher = BcryptHasher(rounds=rounds)

    start = time.time()
    hasher.hash("test_password")
    elapsed = time.time() - start

    print(f"Rounds {rounds}: {elapsed:.3f}s")
```

### Choosing Rounds

- **10 rounds**: Fast but minimal security (legacy systems)
- **12 rounds**: Good balance (recommended for most applications)
- **14 rounds**: Higher security (financial/sensitive data)
- **16+ rounds**: Maximum security (acceptable UX impact for very sensitive systems)

## Hash Format

Bcrypt hashes have the following format:

```
$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW
└┬┘└┬┘└──────────┬───────────┘└───────────┬──────────────────┘
 │  │          Salt               Hash
 │  Rounds
 Prefix
```

**Components:**

- **Prefix**: `$2b$` - Algorithm version
- **Rounds**: `12$` - Cost factor
- **Salt**: 22 characters - Random salt (base64)
- **Hash**: 31 characters - Password hash (base64)

## Complete Authentication Example

```python
from rick.crypto import BcryptHasher


class UserAuthentication:
    def __init__(self):
        self.hasher = BcryptHasher(rounds=12)

    def register(self, username, password):
        """Register a new user"""
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password too short")

        # Hash password
        pw_hash = self.hasher.hash(password)

        # Store username and pw_hash in database
        return {
            'username': username,
            'password_hash': pw_hash
        }

    def login(self, username, password, stored_hash):
        """Authenticate user login"""
        # Verify password
        if not self.hasher.is_valid(password, stored_hash):
            return None

        # Check if hash needs upgrade
        if self.hasher.need_rehash(stored_hash):
            new_hash = self.hasher.hash(password)
            # Update database with new_hash
            return {
                'authenticated': True,
                'rehash_needed': new_hash
            }

        return {
            'authenticated': True,
            'rehash_needed': None
        }


# Usage
auth = UserAuthentication()

# Registration
user = auth.register("alice", "SecureP@ssw0rd!")

# Login
result = auth.login("alice", "SecureP@ssw0rd!", user['password_hash'])
if result and result['authenticated']:
    if result['rehash_needed']:
        # Update database with new hash
        pass
```

## Password Policy Implementation

```python
from rick.crypto import BcryptHasher
import re


class PasswordPolicy:
    def __init__(self, min_length=8, require_upper=True,
                 require_lower=True, require_digit=True,
                 require_special=True):
        self.hasher = BcryptHasher(rounds=12)
        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digit = require_digit
        self.require_special = require_special

    def validate(self, password):
        """Validate password against policy"""
        errors = []

        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")

        if self.require_upper and not re.search(r'[A-Z]', password):
            errors.append("Password must contain uppercase letter")

        if self.require_lower and not re.search(r'[a-z]', password):
            errors.append("Password must contain lowercase letter")

        if self.require_digit and not re.search(r'\d', password):
            errors.append("Password must contain digit")

        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain special character")

        return len(errors) == 0, errors

    def hash_password(self, password):
        """Hash password if it meets policy"""
        is_valid, errors = self.validate(password)
        if not is_valid:
            raise ValueError("Password policy violations: " + "; ".join(errors))

        return self.hasher.hash(password)


# Usage
policy = PasswordPolicy(min_length=10)

try:
    pw_hash = policy.hash_password("MyP@ssw0rd123")
    print("Password hashed successfully")
except ValueError as e:
    print(f"Error: {e}")
```

## Migration from Weaker Hashes

If migrating from MD5, SHA-1, or other weak hashes:

```python
from rick.crypto import BcryptHasher
import hashlib


class PasswordMigration:
    def __init__(self):
        self.hasher = BcryptHasher(rounds=12)

    def is_legacy_hash(self, pw_hash):
        """Check if hash is legacy (MD5/SHA)"""
        # MD5 is 32 hex chars, SHA-1 is 40 hex chars
        return len(pw_hash) in [32, 40] and pw_hash.isalnum()

    def verify_and_upgrade(self, password, stored_hash):
        """Verify password and upgrade hash if legacy"""
        if self.is_legacy_hash(stored_hash):
            # Legacy hash - verify with old method
            md5_hash = hashlib.md5(password.encode()).hexdigest()
            if md5_hash == stored_hash:
                # Upgrade to bcrypt
                new_hash = self.hasher.hash(password)
                return {
                    'valid': True,
                    'upgrade_hash': new_hash
                }
            return {'valid': False, 'upgrade_hash': None}
        else:
            # Modern bcrypt hash
            is_valid = self.hasher.is_valid(password, stored_hash)

            # Check if bcrypt needs rehash
            upgrade_hash = None
            if is_valid and self.hasher.need_rehash(stored_hash):
                upgrade_hash = self.hasher.hash(password)

            return {
                'valid': is_valid,
                'upgrade_hash': upgrade_hash
            }


# Usage
migration = PasswordMigration()

# Legacy MD5 hash
legacy_hash = "5f4dcc3b5aa765d61d8327deb882cf99"  # password: "password"
result = migration.verify_and_upgrade("password", legacy_hash)

if result['valid'] and result['upgrade_hash']:
    # Update database with bcrypt hash
    print("Upgraded to bcrypt:", result['upgrade_hash'])
```

### Timing Attacks

BcryptHasher uses `hmac.compare_digest()` for constant-time comparison:

```python
# Secure implementation (used internally)
import hmac

return hmac.compare_digest(hash1, hash2)

# Insecure comparison (DON'T use)
return hash1 == hash2  # Vulnerable to timing attacks
```

## Performance Considerations

### Login Performance

```python
from rick.crypto import BcryptHasher
import time

hasher = BcryptHasher(rounds=12)

# Hashing is intentionally slow
start = time.time()
pw_hash = hasher.hash("password")
print(f"Hash time: {time.time() - start:.3f}s")

# Verification has same cost
start = time.time()
hasher.is_valid("password", pw_hash)
print(f"Verify time: {time.time() - start:.3f}s")
```

## Error Handling

```python
from rick.crypto import BcryptHasher

hasher = BcryptHasher(rounds=12)

try:
    # Empty password
    hasher.hash("")
except ValueError as e:
    print(f"Invalid password: {e}")

try:
    # Invalid hash format
    hasher.need_rehash("invalid_hash")
except ValueError as e:
    print(f"Invalid hash: {e}")

# Verification never raises (returns False instead)
is_valid = hasher.is_valid("password", "malformed_hash")
print(is_valid)  # False
```

## Related

- **[Fernet256](fernet256.md)** - Symmetric encryption
- **[Buffer Hashing](buffer.md)** - Hash utilities
- **[HasherInterface](#hasherinterface)** - Hasher interface

## HasherInterface

BcryptHasher implements the HasherInterface protocol:

```python
class HasherInterface:
    def hash(self, password: str) -> str:
        """Hash a password"""
        pass

    def is_valid(self, password: str, pw_hash: str) -> bool:
        """Verify password against hash"""
        pass

    def need_rehash(self, pw_hash, prefix=None):
        """Check if hash needs upgrade"""
        pass
```

This allows you to create custom hashers or swap implementations.
