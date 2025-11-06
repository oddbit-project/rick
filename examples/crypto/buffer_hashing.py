"""
Buffer hashing examples with SHA-256, SHA-512, SHA-1, and BLAKE2

This example demonstrates:
- Basic hashing with different algorithms
- File integrity verification
- Duplicate detection
- Content addressing
"""

from rick.crypto import sha256_hash, sha512_hash, sha1_hash, blake2_hash
from rick.crypto.buffer import hash_buffer
from io import BytesIO
import time
import os
import tempfile


def basic_hashing():
    """Basic hashing with different algorithms"""
    print("=== Basic Hashing ===")

    data = b"Hello, World!"
    buffer = BytesIO(data)

    # SHA-256
    buffer.seek(0)
    hash_256 = sha256_hash(buffer)
    print(f"Data: {data.decode('utf-8')}")
    print(f"SHA-256: {hash_256}")

    # SHA-512
    buffer.seek(0)
    hash_512 = sha512_hash(buffer)
    print(f"SHA-512: {hash_512}")

    # SHA-1
    buffer.seek(0)
    hash_1 = sha1_hash(buffer)
    print(f"SHA-1:   {hash_1}")

    # BLAKE2
    buffer.seek(0)
    hash_blake2 = blake2_hash(buffer)
    print(f"BLAKE2:  {hash_blake2}")

    print()


def compare_algorithms():
    """Compare different hash algorithms"""
    print("=== Algorithm Comparison ===")

    # Generate test data (1 MB)
    test_data = b"x" * (1024 * 1024)
    buffer = BytesIO(test_data)

    algorithms = [
        ("SHA-1", sha1_hash, 40),
        ("SHA-256", sha256_hash, 64),
        ("SHA-512", sha512_hash, 128),
        ("BLAKE2", blake2_hash, 128),
    ]

    print(f"Test data size: {len(test_data):,} bytes\n")
    print(f"{'Algorithm':<10} {'Time':<12} {'Length':<8} {'Hash'}")
    print("-" * 70)

    for name, hash_func, expected_len in algorithms:
        buffer.seek(0)
        start = time.time()
        hash_value = hash_func(buffer)
        elapsed = time.time() - start

        print(f"{name:<10} {elapsed*1000:>8.2f}ms   {len(hash_value):<8} {hash_value[:32]}...")

    print()


def file_hashing():
    """Hash files for integrity verification"""
    print("=== File Hashing ===")

    # Create temporary test files
    test_files = []
    for i, content in enumerate([b"File 1 content", b"File 2 content", b"File 1 content"]):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
            f.write(content)
            test_files.append((f.name, content))

    # Hash each file
    file_hashes = {}
    print("Hashing files:")
    for file_path, content in test_files:
        with open(file_path, 'rb') as f:
            buffer = BytesIO(f.read())
            file_hash = sha256_hash(buffer)
            file_hashes[file_path] = file_hash
            print(f"  {os.path.basename(file_path)}: {file_hash[:32]}...")

    # Verify files
    print("\nVerifying file integrity:")
    for file_path, expected_content in test_files:
        with open(file_path, 'rb') as f:
            buffer = BytesIO(f.read())
            computed_hash = sha256_hash(buffer)

        is_valid = computed_hash == file_hashes[file_path]
        print(f"  {os.path.basename(file_path)}: {'VALID' if is_valid else 'INVALID'}")

    # Detect duplicates
    print("\nDetecting duplicates:")
    hash_to_files = {}
    for file_path, file_hash in file_hashes.items():
        if file_hash not in hash_to_files:
            hash_to_files[file_hash] = []
        hash_to_files[file_hash].append(file_path)

    for file_hash, files in hash_to_files.items():
        if len(files) > 1:
            print(f"  Duplicate found (hash: {file_hash[:16]}...):")
            for f in files:
                print(f"    - {os.path.basename(f)}")

    # Cleanup
    for file_path, _ in test_files:
        os.unlink(file_path)

    print()


def content_addressing():
    """Content-addressable storage system"""
    print("=== Content Addressing ===")

    class ContentStore:
        def __init__(self, storage_dir):
            self.storage_dir = storage_dir
            os.makedirs(storage_dir, exist_ok=True)
            self.index = {}  # hash -> metadata

        def store(self, data, metadata=None):
            """Store data and return its hash"""
            buffer = BytesIO(data)
            content_hash = sha256_hash(buffer)

            # Store using hash as filename
            file_path = os.path.join(self.storage_dir, content_hash)
            with open(file_path, 'wb') as f:
                f.write(data)

            # Store metadata
            self.index[content_hash] = metadata or {}

            return content_hash

        def retrieve(self, content_hash):
            """Retrieve data by hash"""
            file_path = os.path.join(self.storage_dir, content_hash)
            if not os.path.exists(file_path):
                return None

            with open(file_path, 'rb') as f:
                return f.read()

        def verify(self, content_hash):
            """Verify stored content integrity"""
            data = self.retrieve(content_hash)
            if data is None:
                return False

            buffer = BytesIO(data)
            computed_hash = sha256_hash(buffer)
            return computed_hash == content_hash

    # Create content store
    storage_dir = tempfile.mkdtemp()
    store = ContentStore(storage_dir)

    # Store documents
    documents = [
        (b"Important document 1", {'type': 'contract', 'version': 1}),
        (b"Meeting notes", {'type': 'notes', 'date': '2025-01-15'}),
        (b"Important document 1", {'type': 'contract', 'version': 2}),
    ]

    print("Storing documents:")
    stored_hashes = []
    for data, metadata in documents:
        content_hash = store.store(data, metadata)
        stored_hashes.append(content_hash)
        print(f"  Stored: {metadata}")
        print(f"    Hash: {content_hash[:32]}...")

    # Retrieve and verify
    print("\nRetrieving and verifying:")
    for content_hash in set(stored_hashes):
        data = store.retrieve(content_hash)
        is_valid = store.verify(content_hash)
        print(f"  Hash: {content_hash[:16]}...")
        print(f"    Data: {data[:30]}...")
        print(f"    Valid: {'VALID' if is_valid else 'INVALID'}")

    # Note deduplication
    print(f"\nDeduplication:")
    print(f"  Documents stored: {len(documents)}")
    print(f"  Unique documents: {len(set(stored_hashes))}")
    print(f"  Space saved: {len(documents) - len(set(stored_hashes))} duplicate(s)")

    # Cleanup
    import shutil
    shutil.rmtree(storage_dir)

    print()


def data_validation():
    """Data validation with checksums"""
    print("=== Data Validation ===")

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

    # Create data with checksum
    original_data = b"Critical configuration data"
    checksum = DataValidator.create_checksum(original_data)

    print(f"Original data: {original_data.decode('utf-8')}")
    print(f"Checksum: {checksum[:32]}...")

    # Validate unchanged data
    print("\nValidating unchanged data:")
    is_valid = DataValidator.validate(original_data, checksum)
    print(f"  Result: {'VALID' if is_valid else 'INVALID'}")

    # Validate corrupted data
    print("\nValidating corrupted data:")
    corrupted_data = b"Critical configuration date"  # 'date' instead of 'data'
    is_valid = DataValidator.validate(corrupted_data, checksum)
    print(f"  Result: {'VALID' if is_valid else 'INVALID'}")

    # Show detection of subtle changes
    print("\nDetecting subtle changes:")
    variations = [
        b"Critical configuration data",
        b"Critical configuration data ",  # Extra space
        b"Critical Configuration Data",  # Different case
        b"critical configuration data",  # Lowercase
    ]

    for i, data in enumerate(variations, 1):
        is_valid = DataValidator.validate(data, checksum)
        status = "VALID" if is_valid else "INVALID"
        print(f"  Variation {i}: {status}")
        if not is_valid:
            print(f"    '{data.decode('utf-8')}'")

    print()


def generic_hash_buffer():
    """Using generic hash_buffer function"""
    print("=== Generic Hash Buffer ===")

    data = BytesIO(b"Test data for hashing")

    algorithms = ["md5", "sha1", "sha256", "sha384", "sha512", "blake2b"]

    print("Testing different algorithms:\n")
    for algo in algorithms:
        try:
            data.seek(0)
            hash_value = hash_buffer(algo, data)
            print(f"{algo.upper():<12} ({len(hash_value)} chars): {hash_value[:40]}...")
        except Exception as e:
            print(f"{algo.upper():<12} Error: {e}")

    print()


if __name__ == '__main__':
    print("Buffer Hashing Examples\n")
    basic_hashing()
    compare_algorithms()
    file_hashing()
    content_addressing()
    data_validation()
    generic_hash_buffer()
