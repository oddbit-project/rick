"""
Basic BcryptHasher password hashing examples

This example demonstrates:
- Hashing passwords
- Verifying passwords
- Rehash detection
- Different rounds (work factors)
"""

from rick.crypto import BcryptHasher
import time


def basic_hashing():
    """Basic password hashing and verification"""
    print("=== Basic Password Hashing ===")

    hasher = BcryptHasher(rounds=12)

    # Hash a password
    password = "my_secure_password_123"
    pw_hash = hasher.hash(password)

    print(f"Password: {password}")
    print(f"Hash: {pw_hash}")
    print(f"Hash length: {len(pw_hash)} characters")

    # Verify correct password
    is_valid = hasher.is_valid(password, pw_hash)
    print(f"\nVerifying correct password: {is_valid}")

    # Verify incorrect password
    is_valid = hasher.is_valid("wrong_password", pw_hash)
    print(f"Verifying wrong password: {is_valid}")

    print()


def different_rounds():
    """Compare different work factors (rounds)"""
    print("=== Different Work Factors ===")

    test_password = "test_password_123"

    for rounds in [10, 12, 14]:
        hasher = BcryptHasher(rounds=rounds)

        # Time the hashing
        start = time.time()
        pw_hash = hasher.hash(test_password)
        elapsed = time.time() - start

        print(f"Rounds: {rounds}")
        print(f"  Time: {elapsed*1000:.1f}ms")
        print(f"  Hash: {pw_hash[:29]}...")
        print()


def rehash_detection():
    """Detect when password hashes need upgrading"""
    print("=== Rehash Detection ===")

    # Create hash with 12 rounds
    hasher_12 = BcryptHasher(rounds=12)
    old_hash = hasher_12.hash("user_password")
    print(f"Created hash with 12 rounds: {old_hash[:29]}...")

    # Check with hasher using 12 rounds (no rehash needed)
    print(f"\nChecking with 12 rounds hasher:")
    print(f"  Need rehash: {hasher_12.need_rehash(old_hash)}")

    # Check with hasher using 14 rounds (rehash needed)
    hasher_14 = BcryptHasher(rounds=14)
    print(f"\nChecking with 14 rounds hasher:")
    print(f"  Need rehash: {hasher_14.need_rehash(old_hash)}")

    # Upgrade the hash
    if hasher_14.need_rehash(old_hash):
        new_hash = hasher_14.hash("user_password")
        print(f"  New hash: {new_hash[:29]}...")

    print()


def hash_format():
    """Understanding bcrypt hash format"""
    print("=== Bcrypt Hash Format ===")

    hasher = BcryptHasher(rounds=12)
    pw_hash = hasher.hash("password")

    print(f"Full hash: {pw_hash}")
    print(f"\nFormat breakdown:")
    print(f"  $2b$        - Prefix (algorithm version)")
    print(f"  12$         - Rounds (work factor)")
    print(f"  [22 chars]  - Salt (base64)")
    print(f"  [31 chars]  - Hash (base64)")

    # Extract components
    parts = pw_hash.split('$')
    print(f"\nExtracted parts:")
    print(f"  Prefix: ${parts[1]}$")
    print(f"  Rounds: ${parts[2]}$")
    print(f"  Salt+Hash: {parts[3][:22]} + {parts[3][22:]}")

    print()


def multiple_hashes():
    """Same password produces different hashes"""
    print("=== Multiple Hashes ===")

    hasher = BcryptHasher(rounds=12)
    password = "same_password"

    print(f"Password: {password}\n")
    print("Hashing the same password 3 times:")

    for i in range(3):
        pw_hash = hasher.hash(password)
        print(f"  {i+1}. {pw_hash}")

    print("\nNote: Different hashes due to random salt,")
    print("      but all verify correctly:")

    # Verify each hash
    for i in range(3):
        pw_hash = hasher.hash(password)
        is_valid = hasher.is_valid(password, pw_hash)
        print(f"  Hash {i+1} verifies: {is_valid}")

    print()


def password_strength():
    """Test password validation"""
    print("=== Password Strength ===")

    hasher = BcryptHasher(rounds=12)

    passwords = [
        "weak",
        "password123",
        "MyP@ssw0rd!",
        "correct horse battery staple",
        "Tr0ub4dor&3"
    ]

    print("Testing different passwords:\n")
    for pwd in passwords:
        # Hash password
        pw_hash = hasher.hash(pwd)

        # Basic strength check
        length = len(pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(not c.isalnum() for c in pwd)

        strength = sum([
            length >= 8,
            length >= 12,
            has_upper,
            has_lower,
            has_digit,
            has_special
        ])

        strength_label = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'][strength]

        print(f"Password: {pwd}")
        print(f"  Length: {length}, Strength: {strength_label}")
        print(f"  Hash: {pw_hash[:40]}...")
        print()


if __name__ == '__main__':
    print("BcryptHasher Basic Examples\n")
    basic_hashing()
    different_rounds()
    rehash_detection()
    hash_format()
    multiple_hashes()
    password_strength()
