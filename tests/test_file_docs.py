"""
Test code samples from docs/resources/file.md
"""
import os
import tempfile
from io import BytesIO
from pathlib import Path

import pytest

from rick.crypto import sha256_hash
from rick.resource.file import FileReader, FilePart


class TestFileDocsBasicUsage:
    """Test basic usage examples from documentation"""

    def test_filereader_basic(self):
        """Test basic FileReader usage"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = Path(tmpdir) / 'file1.dat'
            file2 = Path(tmpdir) / 'file2.dat'
            file1.write_bytes(b'Hello ')
            file2.write_bytes(b'World!')

            # Create parts
            parts = [
                FilePart(str(file1)),
                FilePart(str(file2)),
            ]

            # Create file reader with metadata
            reader = FileReader(
                parts=parts,
                name='document.pdf',
                content_type='application/pdf'
            )

            # Access metadata
            assert reader.name == 'document.pdf'
            assert reader.content_type == 'application/pdf'
            assert reader.size == 12

            # Read entire file as BytesIO
            buffer = reader.read_block()
            assert buffer.getbuffer().nbytes == 12
            buffer.seek(0)  # Reset position to read
            assert buffer.read() == b'Hello World!'

    def test_filereader_chunked(self):
        """Test chunked reading"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / 'test.dat'
            test_data = b'x' * 10000
            test_file.write_bytes(test_data)

            parts = [FilePart(str(test_file))]
            reader = FileReader(parts=parts)

            # Read in fixed-size chunks
            chunks = []
            for chunk in reader.read_chunked(1024):
                chunks.append(chunk.read())

            # Verify all data read
            assert b''.join(chunks) == test_data
            assert len(chunks) == 10  # 10000 / 1024 = 9 full + 1 partial


class TestFileDocsExamples:
    """Test examples from documentation"""

    def test_simple_file_reading(self):
        """Test simple file reading example"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create source file
            source = Path(tmpdir) / 'document.pdf'
            source.write_bytes(b'PDF content here')

            # Read a single file
            parts = [FilePart(str(source))]
            reader = FileReader(
                parts=parts,
                name='document.pdf',
                content_type='application/pdf'
            )

            # Read entire file to disk
            dest = Path(tmpdir) / 'copy.pdf'
            with open(dest, 'wb') as output:
                buffer = reader.read_block()
                buffer.seek(0)  # Reset position to read
                output.write(buffer.read())

            assert dest.read_bytes() == b'PDF content here'
            assert reader.size == 16

    def test_multipart_file_reading(self):
        """Test multipart file reading example"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create split files
            part1 = Path(tmpdir) / 'video.mp4.part1'
            part2 = Path(tmpdir) / 'video.mp4.part2'
            part3 = Path(tmpdir) / 'video.mp4.part3'

            part1.write_bytes(b'a' * 1000)
            part2.write_bytes(b'b' * 1000)
            part3.write_bytes(b'c' * 1000)

            # Read file split into multiple parts
            parts = [
                FilePart(str(part1)),
                FilePart(str(part2)),
                FilePart(str(part3)),
            ]

            reader = FileReader(
                parts=parts,
                name='video.mp4',
                content_type='video/mp4'
            )

            # Combine parts into single file
            output_file = Path(tmpdir) / 'video.mp4'
            with open(output_file, 'wb') as output:
                for chunk in reader.read_chunked(512):
                    output.write(chunk.read())

            assert output_file.read_bytes() == b'a' * 1000 + b'b' * 1000 + b'c' * 1000
            assert reader.size == 3000

    def test_custom_metadata(self):
        """Test custom metadata example"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            photo = Path(tmpdir) / 'photo.jpg'
            photo.write_bytes(b'JPEG data')

            parts = [FilePart(str(photo))]

            reader = FileReader(
                parts=parts,
                name='vacation.jpg',
                content_type='image/jpeg',
                # Custom attributes
                upload_timestamp='2024-01-15 10:30:00',
                user_id=123,
                tags=['vacation', 'beach', 'sunset'],
                metadata={'camera': 'Canon EOS R5', 'iso': 400}
            )

            # Access custom attributes
            assert reader.upload_timestamp == '2024-01-15 10:30:00'
            assert reader.user_id == 123
            assert reader.tags == ['vacation', 'beach', 'sunset']
            assert reader.metadata == {'camera': 'Canon EOS R5', 'iso': 400}

    def test_file_upload_processing(self):
        """Test file upload processing example"""
        with tempfile.TemporaryDirectory() as tmpdir:

            def process_upload(file_parts, filename, content_type):
                """Process uploaded file"""

                reader = FileReader(
                    parts=file_parts,
                    name=filename,
                    content_type=content_type
                )

                # Validate file size
                max_size = 10 * 1024 * 1024  # 10MB
                if reader.size > max_size:
                    raise ValueError(f"File too large: {reader.size} bytes")

                # Calculate hash while saving
                import hashlib
                hasher = hashlib.sha256()
                output_path = f'{tmpdir}/{filename}'

                with open(output_path, 'wb') as output:
                    for chunk in reader.read_chunked(64 * 1024):
                        data = chunk.read()
                        hasher.update(data)
                        output.write(data)

                return {
                    'filename': reader.name,
                    'size': reader.size,
                    'content_type': reader.content_type,
                    'sha256': hasher.hexdigest(),
                    'path': output_path
                }

            # Create test upload
            upload_file = Path(tmpdir) / 'uploaded_file.dat'
            test_data = b'Document content here'
            upload_file.write_bytes(test_data)

            parts = [FilePart(str(upload_file))]
            result = process_upload(parts, 'document.pdf', 'application/pdf')

            assert result['filename'] == 'document.pdf'
            assert result['size'] == len(test_data)
            assert result['content_type'] == 'application/pdf'
            assert len(result['sha256']) == 64  # SHA-256 hex length

    def test_file_validation_and_processing(self):
        """Test file validation and processing example"""
        with tempfile.TemporaryDirectory() as tmpdir:

            def validate_and_process(file_path, expected_hash):
                """Validate file hash and process if valid"""

                parts = [FilePart(file_path)]
                reader = FileReader(
                    parts=parts,
                    name=file_path.split('/')[-1]
                )

                # Read entire file and verify hash
                buffer = reader.read_block()
                actual_hash = sha256_hash(buffer)

                if actual_hash != expected_hash:
                    raise ValueError(
                        f"Hash mismatch: expected {expected_hash}, got {actual_hash}"
                    )

                # Process file in chunks
                buffer.seek(0)
                reader.seek(0)

                results = []
                for chunk in reader.read_chunked(1024):
                    result = len(chunk.read())
                    results.append(result)

                return results

            # Create test file
            test_file = Path(tmpdir) / 'data.bin'
            test_data = b'Test data for validation'
            test_file.write_bytes(test_data)

            # Calculate expected hash
            expected = sha256_hash(BytesIO(test_data))

            # Validate and process
            results = validate_and_process(str(test_file), expected)
            assert sum(results) == len(test_data)

            # Test with wrong hash
            with pytest.raises(ValueError, match="Hash mismatch"):
                validate_and_process(str(test_file), 'a' * 64)

    def test_combining_multiple_files(self):
        """Test combining multiple files example"""
        with tempfile.TemporaryDirectory() as tmpdir:

            def combine_logs(log_directory, output_file):
                """Combine multiple log files into one"""

                # Find all log files
                log_dir = Path(log_directory)
                log_files = sorted(log_dir.glob('*.log'))

                if not log_files:
                    raise ValueError("No log files found")

                # Create parts
                parts = [FilePart(str(f)) for f in log_files]

                # Create reader
                reader = FileReader(
                    parts=parts,
                    name=Path(output_file).name,
                    content_type='text/plain',
                    source_files=[str(f) for f in log_files],
                    file_count=len(log_files)
                )

                # Write combined file
                with open(output_file, 'wb') as output:
                    for chunk in reader.read_chunked(1024):
                        output.write(chunk.read())

                return reader.file_count, reader.size

            # Create test log files
            log_dir = Path(tmpdir) / 'logs'
            log_dir.mkdir()

            (log_dir / '1.log').write_bytes(b'Log 1\n')
            (log_dir / '2.log').write_bytes(b'Log 2\n')
            (log_dir / '3.log').write_bytes(b'Log 3\n')

            # Combine logs
            output = Path(tmpdir) / 'combined.log'
            file_count, total_size = combine_logs(str(log_dir), str(output))

            assert file_count == 3
            assert total_size == 18
            assert output.read_bytes() == b'Log 1\nLog 2\nLog 3\n'


class TestFileDocsPerformance:
    """Test performance examples from documentation"""

    def test_memory_efficiency(self):
        """Test memory efficiency example"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create large file
            large_file = Path(tmpdir) / 'large_file.bin'
            large_file.write_bytes(b'x' * (10 * 1024 * 1024))  # 10MB

            parts = [FilePart(str(large_file))]
            reader = FileReader(parts=parts)

            # Process in 1MB chunks
            backup = Path(tmpdir) / 'backup.bin'
            with open(backup, 'wb') as output:
                for chunk in reader.read_chunked(1024 * 1024):
                    output.write(chunk.read())

            assert backup.read_bytes() == large_file.read_bytes()

    def test_chunk_size_selection(self):
        """Test different chunk sizes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / 'file.bin'
            test_file.write_bytes(b'x' * 10000)

            parts = [FilePart(str(test_file))]
            reader = FileReader(parts=parts)

            # Small chunks (64 bytes)
            chunks_small = list(reader.read_chunked(64))
            assert len(chunks_small) == 157  # 10000 / 64 = 156 + 1

            # Reset reader
            reader.seek(0)

            # Medium chunks (1024 bytes)
            chunks_medium = list(reader.read_chunked(1024))
            assert len(chunks_medium) == 10  # 10000 / 1024 = 9 + 1

    def test_read_block_vs_read_chunked(self):
        """Test read_block() vs read_chunked()"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / 'file.bin'
            test_data = b'Test data content'
            test_file.write_bytes(test_data)

            parts = [FilePart(str(test_file))]
            reader = FileReader(parts=parts)

            # Small file - read_block()
            if reader.size < 10 * 1024 * 1024:
                buffer = reader.read_block()
                buffer.seek(0)  # Reset position to read
                assert buffer.read() == test_data


class TestFileDocsErrorHandling:
    """Test error handling examples from documentation"""

    def test_file_validation_error(self):
        """Test file validation errors"""
        # FilePart validates file exists
        with pytest.raises(ValueError):
            FilePart('/path/to/nonexistent.txt')

    def test_reserved_property_error(self):
        """Test reserved property name conflicts"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'file.txt'
            test_file.write_bytes(b'test')

            parts = [FilePart(str(test_file))]

            # Reserved names raise ValueError (testing actual reserved names)
            with pytest.raises(ValueError, match="invalid custom property name"):
                FileReader(
                    parts=parts,
                    name='test.txt',
                    read=lambda: None  # 'read' is a reserved method name
                )

    def test_seek_error(self):
        """Test seek/read errors"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'file.txt'
            test_file.write_bytes(b'test')

            parts = [FilePart(str(test_file))]
            reader = FileReader(parts=parts)

            # Negative offset raises ValueError
            with pytest.raises(ValueError):
                reader.seek(-100)


class TestFileDocsAPI:
    """Test API reference examples"""

    def test_filereader_constructor(self):
        """Test FileReader constructor"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'test.dat'
            test_file.write_bytes(b'test data')

            parts = [FilePart(str(test_file))]

            reader = FileReader(
                parts=parts,
                name='document.pdf',
                content_type='application/pdf',
                custom_attr='value'
            )

            assert reader.name == 'document.pdf'
            assert reader.content_type == 'application/pdf'
            assert reader.custom_attr == 'value'
            assert reader.size == 9

    def test_read_block_method(self):
        """Test read_block() method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'file.bin'
            test_file.write_bytes(b'abcdefghij')

            reader = FileReader(parts=[FilePart(str(test_file))])

            # Read entire file
            buffer = reader.read_block()
            buffer.seek(0)
            assert buffer.read() == b'abcdefghij'

            # Read first 5 bytes
            buffer = reader.read_block(offset=0, limit=5)
            buffer.seek(0)
            assert buffer.read() == b'abcde'

            # Read 3 bytes starting at position 5
            buffer = reader.read_block(offset=5, limit=3)
            buffer.seek(0)
            assert buffer.read() == b'fgh'

    def test_read_chunked_method(self):
        """Test read_chunked() method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'largefile.bin'
            test_file.write_bytes(b'x' * 5000)

            reader = FileReader(parts=[FilePart(str(test_file))])

            # Process file in 1000 byte chunks
            chunk_count = 0
            total_bytes = 0
            for chunk in reader.read_chunked(1000):
                data = chunk.read()
                total_bytes += len(data)
                chunk_count += 1

            assert chunk_count == 5
            assert total_bytes == 5000

    def test_inherited_methods(self):
        """Test inherited methods from MultiPartReader"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'file.bin'
            test_file.write_bytes(b'0123456789')

            reader = FileReader(parts=[FilePart(str(test_file))])

            # Test seek()
            pos = reader.seek(5)
            assert pos == 5

            # Test seekable()
            assert reader.seekable() is True

            # Test read() - inherited from MultiPartReader
            chunks = list(reader.read(offset=0, length=10))
            assert b''.join(chunks) == b'0123456789'
