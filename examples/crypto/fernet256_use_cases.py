"""
Practical Fernet256 use cases

This example demonstrates:
- Encrypted configuration files
- Session token management
- Encrypted database fields
- Secure API tokens
"""

from rick.crypto import Fernet256
import json
import pickle
import time
import tempfile
import os


class EncryptedConfig:
    """Store configuration securely on disk"""

    def __init__(self, key):
        self.cipher = Fernet256(key)

    def save(self, config, filename):
        """Save encrypted configuration to file"""
        encrypted = self.cipher.encrypt(
            json.dumps(config).encode('utf-8')
        )
        with open(filename, 'wb') as f:
            f.write(encrypted)

    def load(self, filename):
        """Load encrypted configuration from file"""
        with open(filename, 'rb') as f:
            encrypted = f.read()
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode('utf-8'))


class SessionManager:
    """Manage user sessions with encrypted tokens"""

    def __init__(self, secret_key, ttl=3600):
        self.cipher = Fernet256(secret_key)
        self.ttl = ttl  # 1 hour default

    def create_token(self, user_id, data):
        """Create encrypted session token"""
        session = {
            'user_id': user_id,
            'created': int(time.time()),
            'data': data
        }
        return self.cipher.encrypt(pickle.dumps(session))

    def verify_token(self, token):
        """Verify and decode session token"""
        try:
            session = pickle.loads(
                self.cipher.decrypt(token, ttl=self.ttl)
            )
            return session
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None

    def refresh_token(self, old_token):
        """Refresh a valid token with new timestamp"""
        session = self.verify_token(old_token)
        if session:
            # Update timestamp and create new token
            session['created'] = int(time.time())
            return self.cipher.encrypt(pickle.dumps(session))
        return None


class EncryptedDatabase:
    """Simulate encrypted database fields"""

    def __init__(self, key):
        self.cipher = Fernet256(key)
        self.records = {}

    def insert(self, record_id, sensitive_data):
        """Insert record with encrypted fields"""
        encrypted_fields = {}
        for key, value in sensitive_data.items():
            if value is not None:
                encrypted = self.cipher.encrypt(
                    value.encode('utf-8')
                )
                encrypted_fields[key] = encrypted.decode('ascii')
            else:
                encrypted_fields[key] = None

        self.records[record_id] = encrypted_fields

    def get(self, record_id):
        """Retrieve and decrypt record"""
        encrypted = self.records.get(record_id)
        if not encrypted:
            return None

        decrypted = {}
        for key, value in encrypted.items():
            if value is not None:
                decrypted[key] = self.cipher.decrypt(
                    value.encode('ascii')
                ).decode('utf-8')
            else:
                decrypted[key] = None

        return decrypted


class APITokenManager:
    """Manage API tokens with metadata"""

    def __init__(self, secret_key):
        self.cipher = Fernet256(secret_key)

    def create_token(self, api_key, permissions, expires_in=None):
        """Create API token with permissions"""
        token_data = {
            'api_key': api_key,
            'permissions': permissions,
            'created': int(time.time()),
            'expires': int(time.time()) + expires_in if expires_in else None
        }
        return self.cipher.encrypt(json.dumps(token_data).encode('utf-8'))

    def validate_token(self, token, required_permission=None):
        """Validate token and check permissions"""
        try:
            data = json.loads(
                self.cipher.decrypt(token).decode('utf-8')
            )

            # Check expiration
            if data['expires'] and time.time() > data['expires']:
                print("Token expired")
                return None

            # Check permission
            if required_permission:
                if required_permission not in data['permissions']:
                    print(f"Missing permission: {required_permission}")
                    return None

            return data
        except Exception as e:
            print(f"Token validation failed: {e}")
            return None


def demo_encrypted_config():
    """Demonstrate encrypted configuration"""
    print("=== Encrypted Configuration ===")

    key = Fernet256.generate_key()
    config_mgr = EncryptedConfig(key)

    # Configuration with sensitive data
    config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'password': 'super_secret_password'
        },
        'api_keys': {
            'stripe': 'sk_test_123456789',
            'sendgrid': 'SG.abc123def456'
        }
    }

    # Save encrypted
    with tempfile.NamedTemporaryFile(delete=False, suffix='.enc') as tf:
        config_mgr.save(config, tf.name)
        print(f"Saved encrypted config to: {tf.name}")

        # Load encrypted
        loaded = config_mgr.load(tf.name)
        print(f"Loaded config: {json.dumps(loaded, indent=2)}")

        # Cleanup
        os.unlink(tf.name)

    print()


def demo_session_manager():
    """Demonstrate session management"""
    print("=== Session Management ===")

    key = Fernet256.generate_key()
    session_mgr = SessionManager(key, ttl=3600)

    # Create session
    token = session_mgr.create_token(
        user_id=123,
        data={
            'username': 'alice',
            'role': 'admin',
            'preferences': {'theme': 'dark'}
        }
    )
    print(f"Created token: {token.decode('utf-8')[:50]}...")

    # Verify session
    session = session_mgr.verify_token(token)
    if session:
        print(f"Valid session for user: {session['data']['username']}")
        print(f"Role: {session['data']['role']}")

    # Refresh token
    new_token = session_mgr.refresh_token(token)
    print(f"Refreshed token: {new_token.decode('utf-8')[:50]}...")

    print()


def demo_encrypted_database():
    """Demonstrate encrypted database fields"""
    print("=== Encrypted Database Fields ===")

    key = Fernet256.generate_key()
    db = EncryptedDatabase(key)

    # Insert sensitive user data
    db.insert('user_001', {
        'email': 'alice@example.com',
        'phone': '+1-555-0123',
        'ssn': '123-45-6789'
    })
    print("Inserted encrypted record: user_001")

    # Retrieve and decrypt
    user_data = db.get('user_001')
    print(f"Retrieved user data:")
    print(f"  Email: {user_data['email']}")
    print(f"  Phone: {user_data['phone']}")
    print(f"  SSN: {user_data['ssn']}")

    # Show that data is encrypted in storage
    encrypted_record = db.records['user_001']
    print(f"\nEncrypted email in storage: {encrypted_record['email'][:50]}...")

    print()


def demo_api_tokens():
    """Demonstrate API token management"""
    print("=== API Token Management ===")

    key = Fernet256.generate_key()
    token_mgr = APITokenManager(key)

    # Create token with permissions
    token = token_mgr.create_token(
        api_key='project_abc123',
        permissions=['read', 'write', 'delete'],
        expires_in=86400  # 24 hours
    )
    print(f"Created API token: {token.decode('utf-8')[:50]}...")

    # Validate with required permission
    data = token_mgr.validate_token(token, required_permission='read')
    if data:
        print(f"Token valid for API key: {data['api_key']}")
        print(f"Permissions: {', '.join(data['permissions'])}")

    # Try invalid permission
    print("\nTrying to validate with 'admin' permission:")
    data = token_mgr.validate_token(token, required_permission='admin')

    print()


if __name__ == '__main__':
    print("Fernet256 Practical Use Cases\n")
    demo_encrypted_config()
    demo_session_manager()
    demo_encrypted_database()
    demo_api_tokens()
