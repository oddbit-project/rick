# File Operations

Rick provides file handling utilities built on top of the stream processing module. The file module offers enhanced file
reading capabilities with metadata support, chunked reading, and multipart file handling.

## Overview

The file module includes:

- **FilePart** - Alias for FileSlice, representing a file part
- **FileReader** - Enhanced multipart file reader with metadata and chunked reading

## Why FileReader?

FileReader extends MultiPartReader with file-specific features:

- Store file metadata (name, content type, custom attributes)
- Read files in fixed-size chunks
- Handle multipart files with metadata
- Process uploaded files or split archives
- Manage file streams with additional context

## FilePart

`FilePart` is an alias for `FileSlice` from the stream module, providing semantic clarity when working with file parts.

```python
from rick.resource.file import FilePart

# Create a file part
part = FilePart('/path/to/file.dat')

# FilePart is identical to FileSlice
print(f"Part size: {part.size} bytes")
```

See [FileSlice documentation](stream.md#fileslice) for detailed usage.

## FileReader

Enhanced file reader with metadata support and chunked reading capabilities.

### Basic Usage

```python
from rick.resource.file import FileReader, FilePart

# Create parts
parts = [
    FilePart('/tmp/file1.dat'),
    FilePart('/tmp/file2.dat'),
]

# Create file reader with metadata
reader = FileReader(
    parts=parts,
    name='document.pdf',
    content_type='application/pdf'
)

# Access metadata
print(f"Filename: {reader.name}")
print(f"Content-Type: {reader.content_type}")
print(f"Total size: {reader.size} bytes")

# Read entire file as BytesIO
buffer = reader.read_block()
print(f"Read {buffer.getbuffer().nbytes} bytes")

# Read in fixed-size chunks
for chunk in reader.read_chunked(1024 * 1024):  # 1MB chunks
    process_chunk(chunk)
```

### Constructor

**FileReader(parts, name="", content_type="application/octet-stream", \*\*kwargs)**

Creates a new FileReader instance with metadata.

**Parameters:**

- `parts` (list): List of FilePart or SliceReader objects
- `name` (str): Filename (default: "")
- `content_type` (str): MIME type (default: "application/octet-stream")
- `**kwargs`: Custom properties to attach to the reader

**Raises:**

- `ValueError`: If a custom property name conflicts with existing attributes

**Attributes:**

- `name`: Filename
- `content_type`: MIME type
- `parts`: List of file parts
- `size`: Total size of all parts
- `offset`: Current stream position
- Custom attributes from kwargs

**Example:**

```python
from rick.resource.file import FileReader, FilePart

parts = [FilePart('/data/video.mp4')]

reader = FileReader(
    parts=parts,
    name='vacation.mp4',
    content_type='video/mp4',
    upload_id='abc123',
    user_id=42
)

print(f"File: {reader.name}")
print(f"Type: {reader.content_type}")
print(f"Upload ID: {reader.upload_id}")
print(f"User ID: {reader.user_id}")
```

### Methods

#### read_block(offset=0, limit=-1) -> BytesIO

Read data as a single BytesIO buffer.

**Parameters:**

- `offset` (int): Starting byte position (default: 0)
- `limit` (int): Number of bytes to read (default: -1 for all)

**Returns:**

- `BytesIO`: Buffer containing the read data (position at end, use seek(0) to read)

**Example:**

```python
reader = FileReader(parts=[FilePart('/data/file.bin')])

# Read entire file
buffer = reader.read_block()
buffer.seek(0)  # Reset position to beginning
data = buffer.read()

# Read first 1KB
buffer = reader.read_block(offset=0, limit=1024)
buffer.seek(0)
header = buffer.read()

# Read 1KB starting at position 1000
buffer = reader.read_block(offset=1000, limit=1024)
buffer.seek(0)
chunk = buffer.read()
```

#### read_chunked(block_size: int) -> Iterator[BytesIO]

Read file in fixed-size chunks as BytesIO buffers.

**Parameters:**

- `block_size` (int): Size of each chunk in bytes

**Returns:**

- Iterator yielding `BytesIO`: Buffers of size block_size (last chunk may be smaller)

**Example:**

```python
reader = FileReader(parts=[FilePart('/data/largefile.bin')])

# Process file in 1MB chunks
chunk_size = 1024 * 1024
for chunk in reader.read_chunked(chunk_size):
    data = chunk.read()
    process_data(data)
    print(f"Processed {len(data)} bytes")
```

### Inherited Methods

FileReader inherits all methods from MultiPartReader:

- `read(offset, length)` - Read as iterator of bytes
- `seek(offset, whence)` - Seek to position
- `seekable()` - Check if seekable (always True)

See [MultiPartReader documentation](stream.md#multipartreader) for details.

## Examples

### Simple File Reading

```python
from rick.resource.file import FileReader, FilePart

# Read a single file
parts = [FilePart('/tmp/document.pdf')]
reader = FileReader(parts=parts, name='document.pdf', content_type='application/pdf')

# Read entire file to disk
with open('/tmp/copy.pdf', 'wb') as output:
    buffer = reader.read_block()
    buffer.seek(0)
    output.write(buffer.read())

print(f"Copied {reader.size} bytes")
```

### Multipart File Reading

```python
from rick.resource.file import FileReader, FilePart

# Read file split into multiple parts
parts = [
    FilePart('/downloads/video.mp4.part1'),
    FilePart('/downloads/video.mp4.part2'),
    FilePart('/downloads/video.mp4.part3'),
]

reader = FileReader(
    parts=parts,
    name='video.mp4',
    content_type='video/mp4'
)

# Combine parts into single file
with open('/videos/video.mp4', 'wb') as output:
    for chunk in reader.read_chunked(1024 * 1024):  # 1MB chunks
        output.write(chunk.read())

print(f"Reassembled {reader.name}: {reader.size} bytes")
```

### Custom Metadata

```python
from rick.resource.file import FileReader, FilePart

parts = [FilePart('/uploads/photo.jpg')]

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
print(f"Uploaded: {reader.upload_timestamp}")
print(f"User: {reader.user_id}")
print(f"Tags: {', '.join(reader.tags)}")
print(f"Camera: {reader.metadata['camera']}")
```

### File Upload Processing

```python
from rick.resource.file import FileReader, FilePart
import hashlib


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
    hasher = hashlib.sha256()
    output_path = f'/uploads/{filename}'

    with open(output_path, 'wb') as output:
        for chunk in reader.read_chunked(64 * 1024):  # 64KB chunks
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


# Example usage
parts = [FilePart('/tmp/uploaded_file.dat')]
result = process_upload(parts, 'document.pdf', 'application/pdf')
print(f"Saved: {result['filename']} ({result['size']} bytes)")
print(f"SHA256: {result['sha256']}")
```

### Chunked File Transfer

```python
from rick.resource.file import FileReader, FilePart


def transfer_file(source_path, destination, chunk_size=1024 * 1024):
    """Transfer file in chunks with progress"""

    parts = [FilePart(source_path)]
    reader = FileReader(parts=parts)

    total_bytes = reader.size
    transferred = 0

    with open(destination, 'wb') as output:
        for chunk in reader.read_chunked(chunk_size):
            data = chunk.read()
            output.write(data)
            transferred += len(data)

            # Progress reporting
            progress = (transferred / total_bytes) * 100
            print(f"\rProgress: {progress:.1f}%", end='')

    print(f"\nTransferred {transferred} bytes")


# Transfer with 2MB chunks
transfer_file('/data/largefile.bin', '/backup/largefile.bin', 2 * 1024 * 1024)
```

### File Validation and Processing

```python
from rick.resource.file import FileReader, FilePart
from rick.crypto import sha256_hash


def validate_and_process(file_path, expected_hash):
    """Validate file hash and process if valid"""

    parts = [FilePart(file_path)]
    reader = FileReader(
        parts=parts,
        name=file_path.split('/')[-1]
    )

    # Read entire file and verify hash
    buffer = reader.read_block()
    buffer.seek(0)
    actual_hash = sha256_hash(buffer)

    if actual_hash != expected_hash:
        raise ValueError(
            f"Hash mismatch: expected {expected_hash}, got {actual_hash}"
        )

    # Process file in chunks
    buffer.seek(0)  # Reset buffer position
    reader.seek(0)  # Reset reader position

    results = []
    for chunk in reader.read_chunked(1024 * 1024):
        result = process_chunk(chunk)
        results.append(result)

    return results


def process_chunk(chunk):
    """Process a chunk of data"""
    data = chunk.read()
    # Your processing logic here
    return len(data)


# Validate and process
results = validate_and_process(
    '/downloads/data.bin',
    'a1b2c3d4e5f6...'  # Expected SHA-256 hash
)
print(f"Processed {len(results)} chunks")
```

### Combining Multiple Files

```python
from rick.resource.file import FileReader, FilePart
from pathlib import Path


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
        for chunk in reader.read_chunked(1024 * 1024):
            output.write(chunk.read())

    print(f"Combined {reader.file_count} files:")
    for f in reader.source_files:
        print(f"  - {f}")
    print(f"Total size: {reader.size} bytes")


# Combine all logs
combine_logs('/var/log/myapp', '/tmp/combined.log')
```

### Archive Extraction Simulation

```python
from rick.resource.file import FileReader, FilePart


def process_split_archive(archive_parts, extract_to):
    """Process split archive files"""

    # Archive split into multiple files
    parts = [FilePart(part) for part in archive_parts]

    reader = FileReader(
        parts=parts,
        name='archive.tar.gz',
        content_type='application/x-tar',
        part_count=len(parts)
    )

    print(f"Processing {reader.part_count}-part archive")
    print(f"Total size: {reader.size} bytes")

    # Save reassembled archive
    archive_path = f"{extract_to}/{reader.name}"
    with open(archive_path, 'wb') as output:
        bytes_written = 0
        for chunk in reader.read_chunked(512 * 1024):  # 512KB chunks
            data = chunk.read()
            output.write(data)
            bytes_written += len(data)

    print(f"Reassembled archive: {archive_path}")
    return archive_path


# Process split archive
parts = [
    '/downloads/archive.tar.gz.001',
    '/downloads/archive.tar.gz.002',
    '/downloads/archive.tar.gz.003',
]
archive = process_split_archive(parts, '/tmp')
```

### Streaming HTTP Upload

```python
from rick.resource.file import FileReader, FilePart


def upload_to_server(file_path, url, chunk_size=1024 * 1024):
    """Upload file to server in chunks"""

    parts = [FilePart(file_path)]
    reader = FileReader(
        parts=parts,
        name=file_path.split('/')[-1],
        content_type='application/octet-stream'
    )

    print(f"Uploading {reader.name} ({reader.size} bytes)")

    uploaded = 0
    for chunk in reader.read_chunked(chunk_size):
        data = chunk.read()

        # Send chunk to server
        response = send_chunk_to_server(url, data)

        if response.status_code != 200:
            raise RuntimeError(f"Upload failed: {response.status_code}")

        uploaded += len(data)
        progress = (uploaded / reader.size) * 100
        print(f"\rProgress: {progress:.1f}%", end='')

    print("\nUpload complete")


def send_chunk_to_server(url, data):
    """Stub for sending data to server"""
    # Your HTTP upload logic here
    pass


# Upload file
upload_to_server('/data/video.mp4', 'https://example.com/upload')
```

### Custom Properties for Processing Context

```python
from rick.resource.file import FileReader, FilePart
from datetime import datetime


def process_with_context(file_path, **context):
    """Process file with additional context"""

    parts = [FilePart(file_path)]

    reader = FileReader(
        parts=parts,
        name=file_path.split('/')[-1],
        content_type='application/octet-stream',
        # Add context as custom properties
        **context
    )

    print(f"Processing: {reader.name}")
    print(f"User: {reader.user_name}")
    print(f"Department: {reader.department}")
    print(f"Priority: {reader.priority}")

    # Process based on context
    if reader.priority == 'high':
        chunk_size = 2 * 1024 * 1024  # 2MB for high priority
    else:
        chunk_size = 512 * 1024  # 512KB for normal

    for chunk in reader.read_chunked(chunk_size):
        process_chunk_with_context(chunk, reader)


def process_chunk_with_context(chunk, reader):
    """Process chunk with reader context"""
    data = chunk.read()
    # Use reader.user_name, reader.department, etc.
    print(f"  Processed {len(data)} bytes for {reader.user_name}")


# Process with context
process_with_context(
    '/uploads/report.pdf',
    user_name='Alice',
    department='Finance',
    priority='high',
    timestamp=datetime.now().isoformat()
)
```

## Performance Considerations

### Memory Efficiency

FileReader uses MultiPartReader internally, providing efficient streaming:

```python
from rick.resource.file import FileReader, FilePart

# Even with a 10GB file, memory usage stays low
parts = [FilePart('/data/huge_10gb_file.bin')]
reader = FileReader(parts=parts)

# Process in 1MB chunks - only 1MB in memory at a time
with open('/backup/huge_10gb_file.bin', 'wb') as output:
    for chunk in reader.read_chunked(1024 * 1024):
        output.write(chunk.read())
        # Memory usage remains constant
```

### Chunk Size Selection

Choose appropriate chunk sizes based on your use case:

```python
from rick.resource.file import FileReader, FilePart

parts = [FilePart('/data/file.bin')]
reader = FileReader(parts=parts)

# Small chunks (64KB) - low memory, more overhead
for chunk in reader.read_chunked(64 * 1024):
    process(chunk)

# Medium chunks (1MB) - balanced
for chunk in reader.read_chunked(1024 * 1024):
    process(chunk)

# Large chunks (10MB) - higher memory, less overhead
for chunk in reader.read_chunked(10 * 1024 * 1024):
    process(chunk)
```

### read_block() vs read_chunked()

Use `read_block()` for small files, `read_chunked()` for large files:

```python
from rick.resource.file import FileReader, FilePart

parts = [FilePart('/data/file.bin')]
reader = FileReader(parts=parts)

# Small file - read_block() is fine
if reader.size < 10 * 1024 * 1024:  # < 10MB
    buffer = reader.read_block()
    buffer.seek(0)
    process_all(buffer.read())

# Large file - use read_chunked()
else:
    for chunk in reader.read_chunked(1024 * 1024):
        process_chunk(chunk.read())
```

## Error Handling

```python
from rick.resource.file import FileReader, FilePart

try:
    # FilePart validates file exists
    parts = [FilePart('/path/to/nonexistent.txt')]
except ValueError as e:
    print(f"File error: {e}")

try:
    parts = [FilePart('/tmp/file.txt')]

    # Reserved names raise ValueError
    reader = FileReader(
        parts=parts,
        name='test.txt',
        size=100  # 'size' is reserved
    )
except ValueError as e:
    print(f"Property error: {e}")

try:
    parts = [FilePart('/tmp/file.txt')]
    reader = FileReader(parts=parts)

    # Seek/read errors from MultiPartReader
    reader.seek(-100)  # Negative offset
except ValueError as e:
    print(f"Seek error: {e}")
```

## API Reference

### FilePart

Alias for FileSlice. See [FileSlice API](stream.md#fileslice).

### FileReader

Inherits from MultiPartReader with additional features.

#### Constructor

| Parameter      | Type | Default                    | Description                          |
|----------------|------|----------------------------|--------------------------------------|
| `parts`        | list | required                   | List of FilePart/SliceReader objects |
| `name`         | str  | ""                         | Filename                             |
| `content_type` | str  | "application/octet-stream" | MIME type                            |
| `**kwargs`     | any  | -                          | Custom properties to attach          |

#### Methods

| Method                      | Returns           | Description                   |
|-----------------------------|-------------------|-------------------------------|
| `read_block(offset, limit)` | BytesIO           | Read as single buffer         |
| `read_chunked(block_size)`  | Iterator[BytesIO] | Read in fixed-size chunks     |
| `read(offset, length)`      | Iterator[bytes]   | Read as iterator (inherited)  |
| `seek(offset, whence)`      | int               | Seek to position (inherited)  |
| `seekable()`                | bool              | Check if seekable (inherited) |

#### Attributes

| Attribute      | Type | Description                         |
|----------------|------|-------------------------------------|
| `name`         | str  | Filename                            |
| `content_type` | str  | MIME type                           |
| `parts`        | list | List of file parts                  |
| `size`         | int  | Total size in bytes                 |
| `offset`       | int  | Current stream position             |
| `opened`       | bool | Whether stream has been read        |
| Custom attrs   | any  | User-defined properties from kwargs |

## See Also

- [Stream Processing](stream.md) - Underlying multipart stream functionality
- [Resources Overview](index.md) - Overview of all resource utilities
- [Redis Cache](redis.md) - Redis caching with serialization
- [Configuration](config.md) - Configuration management
