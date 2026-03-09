"""
Test all crypto examples to ensure they work correctly
"""
import pytest
import sys
import os
import subprocess


class TestCryptoExamples:
    """Test all crypto example scripts"""

    def run_example(self, script_name):
        """Run an example script and return result"""
        script_path = os.path.join('examples', 'crypto', script_name)
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{os.getcwd()}:{env.get('PYTHONPATH', '')}"

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )

        return result

    def test_fernet256_basic(self):
        """Test fernet256_basic.py example"""
        result = self.run_example('fernet256_basic.py')

        assert result.returncode == 0, f"Script failed with error: {result.stderr}"
        assert "Fernet256 Basic Examples" in result.stdout
        assert "Basic Encryption" in result.stdout
        assert "String Encryption" in result.stdout
        assert "JSON Data Encryption" in result.stdout
        assert "TTL Encryption" in result.stdout
        assert "Decrypted: Secret message" in result.stdout

    def test_fernet256_key_rotation(self):
        """Test fernet256_key_rotation.py example"""
        result = self.run_example('fernet256_key_rotation.py')

        assert result.returncode == 0, f"Script failed with error: {result.stderr}"
        assert "Fernet256 Key Rotation Examples" in result.stdout
        assert "Basic MultiFernet256" in result.stdout
        assert "Key Rotation Scenario" in result.stdout
        assert "Gradual Migration Strategy" in result.stdout
        assert "Multiple Environments" in result.stdout
        assert "Successfully decrypted: User session data" in result.stdout
        assert "Production correctly rejects development token" in result.stdout

    def test_fernet256_use_cases(self):
        """Test fernet256_use_cases.py example"""
        result = self.run_example('fernet256_use_cases.py')

        assert result.returncode == 0, f"Script failed with error: {result.stderr}"
        assert "Fernet256 Practical Use Cases" in result.stdout
        assert "Encrypted Configuration" in result.stdout
        assert "Session Management" in result.stdout
        assert "Encrypted Database Fields" in result.stdout
        assert "API Token Management" in result.stdout
        assert "Valid session for user: alice" in result.stdout
        assert "Token valid for API key: project_abc123" in result.stdout

    def test_bcrypt_basic(self):
        """Test bcrypt_basic.py example"""
        result = self.run_example('bcrypt_basic.py')

        assert result.returncode == 0, f"Script failed with error: {result.stderr}"
        assert "BcryptHasher Basic Examples" in result.stdout
        assert "Basic Password Hashing" in result.stdout
        assert "Different Work Factors" in result.stdout
        assert "Rehash Detection" in result.stdout
        assert "Bcrypt Hash Format" in result.stdout
        assert "Verifying correct password: True" in result.stdout
        assert "Verifying wrong password: False" in result.stdout
        assert "Rounds: 10" in result.stdout
        assert "Rounds: 12" in result.stdout
        assert "Rounds: 14" in result.stdout

    def test_bcrypt_authentication(self):
        """Test bcrypt_authentication.py example"""
        result = self.run_example('bcrypt_authentication.py')

        assert result.returncode == 0, f"Script failed with error: {result.stderr}"
        assert "BcryptHasher Authentication Examples" in result.stdout
        assert "Basic Authentication" in result.stdout
        assert "Password Policy" in result.stdout
        assert "Secure User Manager" in result.stdout
        assert "'success': True" in result.stdout
        assert "Username already exists" in result.stdout
        assert "Account locked after 5 failed attempts" in result.stdout
        assert "Password changed successfully" in result.stdout

    def test_buffer_hashing(self):
        """Test buffer_hashing.py example"""
        result = self.run_example('buffer_hashing.py')

        assert result.returncode == 0, f"Script failed with error: {result.stderr}"
        assert "Buffer Hashing Examples" in result.stdout
        assert "Basic Hashing" in result.stdout
        assert "Algorithm Comparison" in result.stdout
        assert "File Hashing" in result.stdout
        assert "Content Addressing" in result.stdout
        assert "Data Validation" in result.stdout
        assert "SHA-256:" in result.stdout
        assert "SHA-512:" in result.stdout
        assert "SHA-1:" in result.stdout
        assert "BLAKE2:" in result.stdout
        assert "VALID" in result.stdout
        assert "INVALID" in result.stdout

    def test_all_examples_no_errors(self):
        """Test that all examples run without errors"""
        examples = [
            'fernet256_basic.py',
            'fernet256_key_rotation.py',
            'fernet256_use_cases.py',
            'bcrypt_basic.py',
            'bcrypt_authentication.py',
            'buffer_hashing.py',
        ]

        for example in examples:
            result = self.run_example(example)
            assert result.returncode == 0, f"{example} failed: {result.stderr}"
            assert len(result.stdout) > 0, f"{example} produced no output"
            assert "Traceback" not in result.stderr, f"{example} has traceback: {result.stderr}"

    def test_examples_output_format(self):
        """Test that examples produce properly formatted output"""
        examples = [
            ('fernet256_basic.py', ['===', 'Encrypted:', 'Decrypted:']),
            ('bcrypt_basic.py', ['===', 'Password:', 'Hash:', 'Verifying']),
            ('buffer_hashing.py', ['===', 'SHA-256:', 'SHA-512:', 'BLAKE2:']),
        ]

        for example, expected_strings in examples:
            result = self.run_example(example)
            assert result.returncode == 0, f"{example} failed"

            for expected in expected_strings:
                assert expected in result.stdout, \
                    f"{example} missing expected output: {expected}"

    def test_examples_demonstrate_features(self):
        """Test that examples demonstrate key features"""
        # Fernet256 should show encryption/decryption
        result = self.run_example('fernet256_basic.py')
        assert "Generated key:" in result.stdout
        assert "Encrypted token:" in result.stdout
        assert "Decrypted:" in result.stdout

        # Bcrypt should show hashing and verification
        result = self.run_example('bcrypt_basic.py')
        assert "$2b$12$" in result.stdout  # Bcrypt hash format
        assert "True" in result.stdout  # Successful verification
        assert "False" in result.stdout  # Failed verification

        # Buffer hashing should show different algorithms
        result = self.run_example('buffer_hashing.py')
        assert "SHA-256:" in result.stdout
        assert "SHA-512:" in result.stdout
        assert "BLAKE2:" in result.stdout

    def test_examples_show_error_handling(self):
        """Test that examples demonstrate proper error handling"""
        # Key rotation should show environment isolation
        result = self.run_example('fernet256_key_rotation.py')
        assert "Production correctly rejects development token" in result.stdout

        # Authentication should show failed login handling
        result = self.run_example('bcrypt_authentication.py')
        assert "Invalid" in result.stdout or "locked" in result.stdout

        # Buffer hashing should show validation failures
        result = self.run_example('buffer_hashing.py')
        assert "INVALID" in result.stdout

    def test_examples_comprehensive_coverage(self):
        """Test that examples cover all major use cases"""
        # Run all examples and collect their output
        all_output = []
        examples = [
            'fernet256_basic.py',
            'fernet256_key_rotation.py',
            'fernet256_use_cases.py',
            'bcrypt_basic.py',
            'bcrypt_authentication.py',
            'buffer_hashing.py',
        ]

        for example in examples:
            result = self.run_example(example)
            all_output.append(result.stdout)

        combined_output = '\n'.join(all_output)

        # Check Fernet256 coverage
        assert "encryption" in combined_output.lower()
        assert "decrypt" in combined_output.lower()  # Matches "Decrypted" and "decryption"
        assert "rotation" in combined_output.lower()
        assert "session" in combined_output.lower()

        # Check Bcrypt coverage
        assert "password" in combined_output.lower()
        assert "hash" in combined_output.lower()
        assert "authentication" in combined_output.lower()
        assert "rounds" in combined_output.lower()

        # Check Buffer hashing coverage
        assert "sha-256" in combined_output.lower()
        assert "sha-512" in combined_output.lower()
        assert "blake2" in combined_output.lower()
        assert "integrity" in combined_output.lower()
