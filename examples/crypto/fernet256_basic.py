"""
Basic Fernet256 encryption and decryption examples

This example demonstrates:
- Key generation
- Encrypting and decrypting data
- String encryption
- Complex data encryption with JSON
"""

from rick.crypto import Fernet256
import json


def basic_encryption():
    """Basic encryption and decryption"""
    print("=== Basic Encryption ===")

    # Generate a new encryption key
    key = Fernet256.generate_key()
    print(f"Generated key: {key.decode('utf-8')[:50]}...")

    # Create cipher
    cipher = Fernet256(key)

    # Encrypt data
    plaintext = b"Secret message"
    token = cipher.encrypt(plaintext)
    print(f"Encrypted token: {token.decode('utf-8')[:50]}...")

    # Decrypt data
    decrypted = cipher.decrypt(token)
    print(f"Decrypted: {decrypted.decode('utf-8')}")
    print()


def string_encryption():
    """Encrypt and decrypt strings"""
    print("=== String Encryption ===")

    key = Fernet256.generate_key()
    cipher = Fernet256(key)

    # Encrypt string
    text = "Hello, World! This is a secret message."
    token = cipher.encrypt(text.encode('utf-8'))
    print(f"Original: {text}")
    print(f"Encrypted: {token.decode('utf-8')[:50]}...")

    # Decrypt to string
    decrypted = cipher.decrypt(token).decode('utf-8')
    print(f"Decrypted: {decrypted}")
    print()


def json_encryption():
    """Encrypt complex data structures with JSON"""
    print("=== JSON Data Encryption ===")

    key = Fernet256.generate_key()
    cipher = Fernet256(key)

    # Complex data structure
    data = {
        'user': 'alice',
        'email': 'alice@example.com',
        'roles': ['admin', 'user'],
        'settings': {
            'theme': 'dark',
            'notifications': True
        }
    }

    # Encrypt
    token = cipher.encrypt(json.dumps(data).encode('utf-8'))
    print(f"Original data: {data}")
    print(f"Encrypted token: {token.decode('utf-8')[:50]}...")

    # Decrypt
    decrypted_data = json.loads(cipher.decrypt(token).decode('utf-8'))
    print(f"Decrypted data: {decrypted_data}")
    print()


def ttl_encryption():
    """Encryption with time-to-live (TTL)"""
    print("=== TTL Encryption ===")

    key = Fernet256.generate_key()
    cipher = Fernet256(key)

    # Encrypt data
    data = b"This token expires in 3600 seconds"
    token = cipher.encrypt(data)
    print(f"Encrypted: {token.decode('utf-8')[:50]}...")

    # Decrypt with TTL (will succeed immediately)
    try:
        decrypted = cipher.decrypt(token, ttl=3600)
        print(f"Decrypted (within TTL): {decrypted.decode('utf-8')}")
    except Exception as e:
        print(f"Decryption failed: {e}")

    # Extract timestamp
    timestamp = cipher.extract_timestamp(token)
    print(f"Token created at timestamp: {timestamp}")
    print()


if __name__ == '__main__':
    print("Fernet256 Basic Examples\n")
    basic_encryption()
    string_encryption()
    json_encryption()
    ttl_encryption()
