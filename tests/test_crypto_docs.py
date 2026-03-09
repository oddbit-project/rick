"""
Test all code examples from docs/crypto/*.md to ensure they work correctly
"""
import pytest
import os
import tempfile
import shutil
from io import BytesIO
from decimal import Decimal
from datetime import datetime
import pickle
import json
import time


class TestCryptoIndexDocs:
    """Test code examples from docs/crypto/index.md"""

    def test_fernet256_basic_example(self):
        """Test basic Fernet256 encryption example"""
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

    def test_bcrypt_basic_example(self):
        """Test basic BcryptHasher example"""
        from rick.crypto import BcryptHasher

        hasher = BcryptHasher(rounds=12)

        # Hash a password
        password = "user_password_123"
        pw_hash = hasher.hash(password)

        # Verify password
        is_valid = hasher.is_valid(password, pw_hash)
        assert is_valid is True

        # Check if rehash needed (for security upgrades)
        # With same rounds, should not need rehash
        assert hasher.need_rehash(pw_hash) is False

    def test_buffer_hashing_example(self):
        """Test buffer hashing example"""
        from rick.crypto import sha256_hash, sha512_hash
        from io import BytesIO

        data = BytesIO(b"Data to hash")

        # SHA-256
        hash_256 = sha256_hash(data)
        assert len(hash_256) == 64  # 256 bits = 64 hex chars

        # SHA-512
        data.seek(0)  # Reset buffer
        hash_512 = sha512_hash(data)
        assert len(hash_512) == 128  # 512 bits = 128 hex chars

    def test_password_management_example(self):
        """Test password management example"""
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

        # Test registration and login
        stored_hash = register_user("alice", "secure_password_123")
        assert login_user("alice", "secure_password_123", stored_hash) is True
        assert login_user("alice", "wrong_password", stored_hash) is False

    def test_file_integrity_verification(self):
        """Test file integrity verification example"""
        from rick.crypto import sha256_hash
        from io import BytesIO

        def verify_file_content(content, expected_hash):
            buffer = BytesIO(content)
            computed_hash = sha256_hash(buffer)
            return computed_hash == expected_hash

        # Test verification
        content = b"File content here"
        buffer = BytesIO(content)
        expected_hash = sha256_hash(buffer)

        assert verify_file_content(content, expected_hash) is True
        assert verify_file_content(b"Different content", expected_hash) is False


class TestFernet256Docs:
    """Test code examples from docs/crypto/fernet256.md"""

    def test_generating_keys(self):
        """Test key generation example"""
        from rick.crypto import Fernet256

        # Generate a new encryption key
        key = Fernet256.generate_key()
        # Returns: base64-encoded 64-byte key
        assert len(key) > 0
        assert isinstance(key, bytes)

    def test_encrypting_data(self):
        """Test encryption example"""
        from rick.crypto import Fernet256

        key = Fernet256.generate_key()
        cipher = Fernet256(key)

        # Encrypt data (must be bytes)
        plaintext = b"Secret message"
        token = cipher.encrypt(plaintext)

        assert token is not None
        assert isinstance(token, bytes)

    def test_decrypting_data(self):
        """Test decryption example"""
        from rick.crypto import Fernet256

        key = Fernet256.generate_key()
        cipher = Fernet256(key)

        plaintext = b"Secret message"
        token = cipher.encrypt(plaintext)

        # Decrypt token
        decrypted = cipher.decrypt(token)

        assert decrypted == b"Secret message"

    def test_ttl_example(self):
        """Test TTL (time-to-live) example"""
        from rick.crypto import Fernet256

        cipher = Fernet256(Fernet256.generate_key())

        # Encrypt data
        data = b"expires soon"
        token = cipher.encrypt(data)

        # Decrypt immediately (works)
        decrypted = cipher.decrypt(token, ttl=5)
        assert decrypted == b"expires soon"

        # Wait 6 seconds would cause failure, but we'll skip the actual wait
        # to keep tests fast

    def test_string_encryption(self):
        """Test string encryption example"""
        from rick.crypto import Fernet256

        cipher = Fernet256(Fernet256.generate_key())

        # Encrypt string
        text = "Hello, World!"
        token = cipher.encrypt(text.encode('utf-8'))

        # Decrypt to string
        decrypted = cipher.decrypt(token).decode('utf-8')
        assert decrypted == text

    def test_encrypting_complex_data_pickle(self):
        """Test encrypting complex data with pickle"""
        from rick.crypto import Fernet256
        import pickle

        cipher = Fernet256(Fernet256.generate_key())

        # Using pickle
        data = {'user': 'alice', 'roles': ['admin', 'user']}
        token = cipher.encrypt(pickle.dumps(data))
        decrypted = pickle.loads(cipher.decrypt(token))

        assert decrypted == data

    def test_encrypting_complex_data_json(self):
        """Test encrypting complex data with JSON"""
        from rick.crypto import Fernet256
        import json

        cipher = Fernet256(Fernet256.generate_key())

        # Using JSON
        data = {'user': 'bob', 'age': 30}
        token = cipher.encrypt(json.dumps(data).encode('utf-8'))
        decrypted = json.loads(cipher.decrypt(token).decode('utf-8'))

        assert decrypted == data

    def test_multifernet256_basic(self):
        """Test MultiFernet256 basic usage"""
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
        assert decrypted == b"data"

    def test_key_rotation(self):
        """Test key rotation example"""
        from rick.crypto import Fernet256, MultiFernet256

        # Current production key
        key_current = Fernet256.generate_key()

        # Encrypt with current key
        cipher_current = Fernet256(key_current)
        old_token = cipher_current.encrypt(b"test data")

        # New key for rotation
        key_new = Fernet256.generate_key()

        # Create multi-fernet with new key first
        multi = MultiFernet256([
            Fernet256(key_new),      # New key (encrypts)
            Fernet256(key_current),  # Old key (decrypts)
        ])

        # Rotate to new key
        new_token = multi.rotate(old_token)

        # New token is now encrypted with key_new
        # Verify with new key cipher
        cipher_new = Fernet256(key_new)
        decrypted = cipher_new.decrypt(new_token)
        assert decrypted == b"test data"

    def test_encrypted_config_use_case(self):
        """Test encrypted configuration use case"""
        from rick.crypto import Fernet256
        import json
        import tempfile

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

        # Test
        key = Fernet256.generate_key()
        config_manager = EncryptedConfig(key)

        config = {'database': 'localhost', 'port': 5432}

        with tempfile.NamedTemporaryFile(delete=False) as tf:
            config_manager.save(config, tf.name)
            loaded_config = config_manager.load(tf.name)
            os.unlink(tf.name)

        assert loaded_config == config

    def test_session_manager_use_case(self):
        """Test session manager use case"""
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
                except Exception:
                    return None

        # Test
        key = Fernet256.generate_key()
        session_mgr = SessionManager(key)

        token = session_mgr.create_token(123, {'role': 'admin'})
        session = session_mgr.verify_token(token)

        assert session is not None
        assert session['user_id'] == 123
        assert session['data'] == {'role': 'admin'}


class TestBcryptDocs:
    """Test code examples from docs/crypto/bcrypt.md"""

    def test_hashing_passwords(self):
        """Test password hashing example"""
        from rick.crypto import BcryptHasher

        hasher = BcryptHasher(rounds=12)

        # Hash a password
        password = "user_password_123"
        pw_hash = hasher.hash(password)

        assert pw_hash is not None
        assert pw_hash.startswith("$2b$12$")

    def test_verifying_passwords(self):
        """Test password verification example"""
        from rick.crypto import BcryptHasher

        hasher = BcryptHasher(rounds=12)

        password = "user_password_123"
        pw_hash = hasher.hash(password)

        # Verify correct password
        is_valid = hasher.is_valid(password, pw_hash)
        assert is_valid is True

        # Verify incorrect password
        is_valid = hasher.is_valid("wrong_password", pw_hash)
        assert is_valid is False

    def test_checking_for_rehash(self):
        """Test rehash detection example"""
        from rick.crypto import BcryptHasher

        # Current hasher with 14 rounds
        hasher = BcryptHasher(rounds=14)

        # Create a hash with 12 rounds for testing
        hasher_12 = BcryptHasher(rounds=12)
        old_hash = hasher_12.hash("test_password")

        # Check if rehash is needed
        assert hasher.need_rehash(old_hash) is True

    def test_user_authentication_class(self):
        """Test complete authentication example"""
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
        assert user['username'] == "alice"

        # Login
        result = auth.login("alice", "SecureP@ssw0rd!", user['password_hash'])
        assert result is not None
        assert result['authenticated'] is True

    def test_password_policy_implementation(self):
        """Test password policy implementation"""
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

        # Test valid password
        pw_hash = policy.hash_password("MyP@ssw0rd123")
        assert pw_hash is not None

        # Test invalid password
        with pytest.raises(ValueError):
            policy.hash_password("short")


class TestBufferDocs:
    """Test code examples from docs/crypto/buffer.md"""

    def test_sha256_basic(self):
        """Test SHA-256 basic example"""
        from rick.crypto import sha256_hash
        from io import BytesIO

        # Hash some data
        data = BytesIO(b"Hello, World!")
        hash_value = sha256_hash(data)

        assert len(hash_value) == 64
        assert hash_value == "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"

    def test_sha512_basic(self):
        """Test SHA-512 basic example"""
        from rick.crypto import sha512_hash
        from io import BytesIO

        data = BytesIO(b"Hello, World!")
        hash_value = sha512_hash(data)

        assert len(hash_value) == 128

    def test_sha1_basic(self):
        """Test SHA-1 basic example"""
        from rick.crypto import sha1_hash
        from io import BytesIO

        data = BytesIO(b"Hello, World!")
        hash_value = sha1_hash(data)

        assert len(hash_value) == 40
        assert hash_value == "0a0a9f2a6772942557ab5355d76af442f8f65e01"

    def test_blake2_basic(self):
        """Test BLAKE2 basic example"""
        from rick.crypto import blake2_hash
        from io import BytesIO

        data = BytesIO(b"Hello, World!")
        hash_value = blake2_hash(data)

        assert len(hash_value) == 128

    def test_hash_buffer_generic(self):
        """Test generic hash_buffer function"""
        from rick.crypto.buffer import hash_buffer
        from io import BytesIO

        data = BytesIO(b"data to hash")

        # Use SHA-256
        sha256 = hash_buffer("sha256", data)
        assert len(sha256) == 64

        # Use SHA-384
        data.seek(0)
        sha384 = hash_buffer("sha384", data)
        assert len(sha384) == 96

    def test_hash_file(self):
        """Test file hashing example"""
        from rick.crypto import sha256_hash
        from io import BytesIO
        import tempfile

        def hash_file(file_path):
            """Compute SHA-256 hash of a file"""
            with open(file_path, 'rb') as f:
                data = BytesIO(f.read())
                return sha256_hash(data)

        # Create temp file and hash it
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"test content")
            tf.flush()

            file_hash = hash_file(tf.name)
            assert len(file_hash) == 64

            os.unlink(tf.name)

    def test_verify_file_integrity(self):
        """Test file integrity verification"""
        from rick.crypto import sha256_hash
        from io import BytesIO
        import tempfile

        def verify_file(file_path, expected_hash):
            with open(file_path, 'rb') as f:
                buffer = BytesIO(f.read())
                computed_hash = sha256_hash(buffer)
                return computed_hash == expected_hash

        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            content = b"test content"
            tf.write(content)
            tf.flush()

            # Compute expected hash
            expected = sha256_hash(BytesIO(content))

            # Verify file
            assert verify_file(tf.name, expected) is True
            assert verify_file(tf.name, "wrong_hash") is False

            os.unlink(tf.name)

    def test_content_store(self):
        """Test content-addressable storage"""
        from rick.crypto import sha256_hash
        from io import BytesIO
        import os
        import tempfile

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
        storage_dir = tempfile.mkdtemp()
        store = ContentStore(storage_dir)

        # Store data
        data = b"Important document content"
        content_id = store.store(data)
        assert len(content_id) == 64

        # Retrieve data
        retrieved = store.retrieve(content_id)
        assert retrieved == data

        # Cleanup
        shutil.rmtree(storage_dir)

    def test_data_validator(self):
        """Test checksum validation"""
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

        # Validate the data
        assert validator.validate(data, checksum) is True
        assert validator.validate(b"Different data", checksum) is False

    def test_find_duplicates(self):
        """Test duplicate file detection"""
        from rick.crypto import sha256_hash
        from io import BytesIO
        import os
        import tempfile

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

        # Create test directory with duplicates
        test_dir = tempfile.mkdtemp()

        with open(os.path.join(test_dir, "file1.txt"), 'wb') as f:
            f.write(b"same content")

        with open(os.path.join(test_dir, "file2.txt"), 'wb') as f:
            f.write(b"same content")

        with open(os.path.join(test_dir, "file3.txt"), 'wb') as f:
            f.write(b"different content")

        # Find duplicates
        dupes = find_duplicates(test_dir)
        assert len(dupes) == 1

        # Cleanup
        shutil.rmtree(test_dir)

    def test_hash_record(self):
        """Test database record hashing"""
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
        assert len(record_hash) == 64

        # Same record should produce same hash
        record_hash2 = hash_record(record)
        assert record_hash == record_hash2

    def test_api_response_validation(self):
        """Test API response validation"""
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
        assert validate_api_response(response, signature) is True
        assert validate_api_response({'status': 'fail'}, signature) is False

    def test_cache_manager(self):
        """Test caching with hash keys"""
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
        assert cached == 'result_data'
