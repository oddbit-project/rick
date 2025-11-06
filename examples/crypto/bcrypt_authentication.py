"""
BcryptHasher authentication system examples

This example demonstrates:
- User registration and login
- Password policy enforcement
- Hash upgrades on login
- Account security features
"""

from rick.crypto import BcryptHasher
import re
from datetime import datetime


class UserAuthentication:
    """Complete user authentication system"""

    def __init__(self, rounds=12):
        self.hasher = BcryptHasher(rounds=rounds)
        self.users = {}  # username -> {'hash': str, 'created': datetime}

    def register(self, username, password):
        """Register a new user"""
        # Check if user exists
        if username in self.users:
            return {'success': False, 'error': 'Username already exists'}

        # Validate password strength
        if len(password) < 8:
            return {'success': False, 'error': 'Password too short (min 8 characters)'}

        # Hash password
        pw_hash = self.hasher.hash(password)

        # Store user
        self.users[username] = {
            'hash': pw_hash,
            'created': datetime.now(),
            'failed_attempts': 0
        }

        return {'success': True, 'message': 'User registered successfully'}

    def login(self, username, password):
        """Authenticate user login"""
        # Check if user exists
        if username not in self.users:
            return {'success': False, 'error': 'Invalid username or password'}

        user = self.users[username]

        # Verify password
        if not self.hasher.is_valid(password, user['hash']):
            # Track failed attempts
            user['failed_attempts'] += 1
            return {'success': False, 'error': 'Invalid username or password'}

        # Reset failed attempts on successful login
        user['failed_attempts'] = 0

        # Check if hash needs upgrade
        rehash_needed = None
        if self.hasher.need_rehash(user['hash']):
            new_hash = self.hasher.hash(password)
            user['hash'] = new_hash
            rehash_needed = True

        return {
            'success': True,
            'message': 'Login successful',
            'rehashed': rehash_needed
        }


class PasswordPolicy:
    """Password policy enforcement"""

    def __init__(self, min_length=8, require_upper=True, require_lower=True,
                 require_digit=True, require_special=True):
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


class SecureUserManager:
    """User manager with security features"""

    def __init__(self):
        self.hasher = BcryptHasher(rounds=12)
        self.policy = PasswordPolicy(min_length=10)
        self.users = {}
        self.max_failed_attempts = 5

    def register(self, username, password):
        """Register user with policy enforcement"""
        # Validate password
        is_valid, errors = self.policy.validate(password)
        if not is_valid:
            return {'success': False, 'errors': errors}

        # Hash password
        pw_hash = self.hasher.hash(password)

        # Store user
        self.users[username] = {
            'hash': pw_hash,
            'created': datetime.now(),
            'failed_attempts': 0,
            'locked': False,
            'last_login': None
        }

        return {'success': True, 'message': 'Registration successful'}

    def login(self, username, password):
        """Login with account lockout protection"""
        if username not in self.users:
            return {'success': False, 'error': 'Invalid credentials'}

        user = self.users[username]

        # Check if account is locked
        if user['locked']:
            return {
                'success': False,
                'error': 'Account locked due to too many failed attempts'
            }

        # Verify password
        if not self.hasher.is_valid(password, user['hash']):
            user['failed_attempts'] += 1

            # Lock account if too many attempts
            if user['failed_attempts'] >= self.max_failed_attempts:
                user['locked'] = True
                return {
                    'success': False,
                    'error': f'Account locked after {self.max_failed_attempts} failed attempts'
                }

            return {
                'success': False,
                'error': f'Invalid credentials ({self.max_failed_attempts - user["failed_attempts"]} attempts remaining)'
            }

        # Successful login
        user['failed_attempts'] = 0
        user['last_login'] = datetime.now()

        # Check for rehash
        if self.hasher.need_rehash(user['hash']):
            user['hash'] = self.hasher.hash(password)

        return {'success': True, 'message': 'Login successful'}

    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if username not in self.users:
            return {'success': False, 'error': 'User not found'}

        user = self.users[username]

        # Verify old password
        if not self.hasher.is_valid(old_password, user['hash']):
            return {'success': False, 'error': 'Invalid current password'}

        # Validate new password
        is_valid, errors = self.policy.validate(new_password)
        if not is_valid:
            return {'success': False, 'errors': errors}

        # Hash new password
        user['hash'] = self.hasher.hash(new_password)

        return {'success': True, 'message': 'Password changed successfully'}


def demo_basic_auth():
    """Demonstrate basic authentication"""
    print("=== Basic Authentication ===")

    auth = UserAuthentication(rounds=12)

    # Register users
    print("\n1. Registering users:")
    result = auth.register("alice", "password123")
    print(f"   alice: {result}")

    result = auth.register("bob", "SecureP@ss456")
    print(f"   bob: {result}")

    # Try duplicate registration
    result = auth.register("alice", "different_password")
    print(f"   alice (duplicate): {result}")

    # Login attempts
    print("\n2. Login attempts:")
    result = auth.login("alice", "password123")
    print(f"   alice (correct): {result}")

    result = auth.login("alice", "wrong_password")
    print(f"   alice (wrong): {result}")

    result = auth.login("bob", "SecureP@ss456")
    print(f"   bob (correct): {result}")

    print()


def demo_password_policy():
    """Demonstrate password policy"""
    print("=== Password Policy ===")

    policy = PasswordPolicy(min_length=10)

    passwords = [
        "weak",
        "password123",
        "MyP@ssw0rd",
        "MyP@ssw0rd123",
    ]

    print("\nTesting passwords against policy:")
    print("(min 10 chars, uppercase, lowercase, digit, special)\n")

    for pwd in passwords:
        is_valid, errors = policy.validate(pwd)
        print(f"Password: {pwd}")
        if is_valid:
            print(f"  Status: VALID")
            pw_hash = policy.hash_password(pwd)
            print(f"  Hash: {pw_hash[:40]}...")
        else:
            print(f"  Status: INVALID")
            for error in errors:
                print(f"    - {error}")
        print()


def demo_secure_manager():
    """Demonstrate secure user manager"""
    print("=== Secure User Manager ===")

    manager = SecureUserManager()

    # Register with strong password
    print("\n1. Registration:")
    result = manager.register("alice", "MyP@ssw0rd123")
    print(f"   Strong password: {result}")

    result = manager.register("bob", "weak")
    print(f"   Weak password: {result}")

    # Successful login
    print("\n2. Successful login:")
    result = manager.login("alice", "MyP@ssw0rd123")
    print(f"   {result}")

    # Failed login attempts
    print("\n3. Failed login attempts:")
    for i in range(6):
        result = manager.login("alice", "wrong_password")
        print(f"   Attempt {i+1}: {result['error']}")
        if manager.users['alice']['locked']:
            break

    # Change password
    print("\n4. Password change:")
    manager2 = SecureUserManager()
    manager2.register("charlie", "OldP@ssw0rd123")

    result = manager2.change_password("charlie", "wrong_old", "NewP@ssw0rd456")
    print(f"   Wrong old password: {result}")

    result = manager2.change_password("charlie", "OldP@ssw0rd123", "NewP@ssw0rd456")
    print(f"   Correct old password: {result}")

    # Verify new password works
    result = manager2.login("charlie", "NewP@ssw0rd456")
    print(f"   Login with new password: {result['message']}")

    print()


if __name__ == '__main__':
    print("BcryptHasher Authentication Examples\n")
    demo_basic_auth()
    demo_password_policy()
    demo_secure_manager()
