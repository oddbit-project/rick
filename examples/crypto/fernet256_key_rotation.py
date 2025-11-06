"""
Fernet256 key rotation with MultiFernet256

This example demonstrates:
- Using MultiFernet256 for key rotation
- Encrypting with primary key
- Decrypting with multiple keys
- Rotating old tokens to new key
"""

from rick.crypto import Fernet256, MultiFernet256
import time


def basic_multifernet():
    """Basic MultiFernet256 usage"""
    print("=== Basic MultiFernet256 ===")

    # Create multiple keys
    key1 = Fernet256.generate_key()
    key2 = Fernet256.generate_key()

    # Create multi-fernet (first key is primary)
    multi = MultiFernet256([
        Fernet256(key1),  # Primary key for encryption
        Fernet256(key2),  # Secondary key for decryption
    ])

    # Encryption always uses primary key (key1)
    data = b"Encrypted with primary key"
    token = multi.encrypt(data)
    print(f"Encrypted: {token.decode('utf-8')[:50]}...")

    # Decryption tries all keys
    decrypted = multi.decrypt(token)
    print(f"Decrypted: {decrypted.decode('utf-8')}")
    print()


def key_rotation_scenario():
    """Simulate key rotation in production"""
    print("=== Key Rotation Scenario ===")

    # Step 1: Current production setup with old key
    print("\n1. Initial setup with old key")
    key_old = Fernet256.generate_key()
    cipher_old = Fernet256(key_old)

    # Encrypt some data with old key
    data = b"User session data"
    old_token = cipher_old.encrypt(data)
    print(f"   Old token: {old_token.decode('utf-8')[:50]}...")

    # Step 2: Generate new key for rotation
    print("\n2. Generate new key")
    key_new = Fernet256.generate_key()
    print(f"   New key generated")

    # Step 3: Deploy MultiFernet with both keys (new key first)
    print("\n3. Deploy MultiFernet with both keys")
    multi = MultiFernet256([
        Fernet256(key_new),      # New key (for encryption)
        Fernet256(key_old),      # Old key (for decryption)
    ])

    # Step 4: Decrypt old token (works because old key is in the list)
    print("\n4. Decrypt old token with MultiFernet")
    decrypted = multi.decrypt(old_token)
    print(f"   Successfully decrypted: {decrypted.decode('utf-8')}")

    # Step 5: New encryptions use new key
    print("\n5. New encryptions use new key")
    new_data = b"New user session"
    new_token = multi.encrypt(new_data)
    print(f"   New token: {new_token.decode('utf-8')[:50]}...")

    # Step 6: Rotate old token to new key
    print("\n6. Rotate old token to new key")
    rotated_token = multi.rotate(old_token)
    print(f"   Rotated token: {rotated_token.decode('utf-8')[:50]}...")

    # Verify rotated token can be decrypted with new key only
    cipher_new = Fernet256(key_new)
    decrypted_rotated = cipher_new.decrypt(rotated_token)
    print(f"   Decrypted with new key: {decrypted_rotated.decode('utf-8')}")
    print()


def gradual_migration():
    """Gradual migration strategy for key rotation"""
    print("=== Gradual Migration Strategy ===")

    # Simulate existing tokens encrypted with old keys
    print("\n1. Existing tokens with old keys")
    key_v1 = Fernet256.generate_key()
    key_v2 = Fernet256.generate_key()
    key_v3 = Fernet256.generate_key()

    # Some users have tokens from different key versions
    cipher_v1 = Fernet256(key_v1)
    cipher_v2 = Fernet256(key_v2)

    user_tokens = {
        'user1': cipher_v1.encrypt(b"user1 data"),
        'user2': cipher_v2.encrypt(b"user2 data"),
        'user3': cipher_v1.encrypt(b"user3 data"),
    }

    print(f"   Created tokens for {len(user_tokens)} users")

    # Create MultiFernet with all historical keys + new key
    print("\n2. Deploy MultiFernet with all keys (newest first)")
    multi = MultiFernet256([
        Fernet256(key_v3),  # New key (v3)
        Fernet256(key_v2),  # Previous key (v2)
        Fernet256(key_v1),  # Oldest key (v1)
    ])

    # Process each user token
    print("\n3. Process and rotate user tokens")
    for user, token in user_tokens.items():
        # Decrypt (works with any of the keys)
        data = multi.decrypt(token)
        print(f"   {user}: {data.decode('utf-8')}")

        # Rotate to new key
        new_token = multi.rotate(token)
        user_tokens[user] = new_token

    print("\n4. All tokens now use new key (v3)")
    print("   Old keys (v1, v2) can be retired after all tokens are rotated")
    print()


def multiple_environments():
    """Using different keys for different environments"""
    print("=== Multiple Environments ===")

    # Different keys for different environments
    key_dev = Fernet256.generate_key()
    key_staging = Fernet256.generate_key()
    key_production = Fernet256.generate_key()

    print("Generated keys for:")
    print("  - Development")
    print("  - Staging")
    print("  - Production")

    # Each environment has its own cipher
    cipher_dev = Fernet256(key_dev)
    cipher_prod = Fernet256(key_production)

    # Encrypt in dev
    data = b"Configuration data"
    dev_token = cipher_dev.encrypt(data)
    print(f"\nDevelopment token: {dev_token.decode('utf-8')[:50]}...")

    # This token cannot be decrypted in production
    # (demonstrates environment isolation)
    try:
        cipher_prod.decrypt(dev_token)
        print("ERROR: Should not decrypt!")
    except Exception:
        print("Production correctly rejects development token")

    # Encrypt in production
    prod_token = cipher_prod.encrypt(data)
    print(f"Production token: {prod_token.decode('utf-8')[:50]}...")
    print()


if __name__ == '__main__':
    print("Fernet256 Key Rotation Examples\n")
    basic_multifernet()
    key_rotation_scenario()
    gradual_migration()
    multiple_environments()
