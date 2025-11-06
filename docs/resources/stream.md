# Stream Processing

Rick provides stream processing utilities for handling multipart data streams with minimal memory usage. The stream
module is designed for efficiently reading data from multiple sources (files, memory buffers) as a unified stream with
seek support.

## Overview

The stream module includes:

- **SliceReader** - Abstract base class for reading data slices
- **FileSlice** - Read file slices from disk
- **BytesIOSlice** - Read slices from memory buffers
- **MultiPartReader** - Combine multiple slices into a single seekable stream

## Why MultiPartReader?

When working with large files or multipart data, loading everything into memory is inefficient. MultiPartReader allows
you to:

- Read data from multiple sources as a unified stream
- Seek to specific positions without loading entire file
- Process large files with minimal memory footprint
- Combine file chunks, memory buffers, and other data sources
- Stream data efficiently for uploads, downloads, or processing

## SliceReader Base Class

`SliceReader` is the abstract base class for all slice implementations.

```python
from rick.resource.stream import SliceReader


class SliceReader:
    def __init__(self, identifier, size: int = 0):
        self.identifier = identifier
        self.size = size

    def read(self, offset=0, length=-1):
        """Read data from slice

        Args:
            offset: Starting position (default: 0)
            length: Number of bytes to read (default: -1 for all)

        Returns:
            bytes: Data read from slice
        """
        pass
```

## FileSlice

Read slices from files on disk.

### Basic Usage

```python
from rick.resource.stream import FileSlice

# Create a file slice
file_slice = FileSlice('/path/to/file.dat')

# Get file size
print(f"File size: {file_slice.size} bytes")

# Read entire file
data = file_slice.read()

# Read first 100 bytes
data = file_slice.read(offset=0, length=100)

# Read 50 bytes starting at position 1000
data = file_slice.read(offset=1000, length=50)
```

### Constructor

**FileSlice(file_path: str)**

Creates a new FileSlice instance.

**Parameters:**

- `file_path` (str): Path to the file

**Raises:**

- `ValueError`: If file does not exist or is not a regular file

**Attributes:**

- `identifier`: Path object pointing to the file
- `size`: File size in bytes

### Methods

**read(offset=0, length=-1) -> bytes**

Read data from the file.

**Parameters:**

- `offset` (int): Starting byte position (default: 0)
- `length` (int): Number of bytes to read (default: -1 for entire file)

**Returns:**

- `bytes`: Data read from file

## BytesIOSlice

Read slices from BytesIO memory buffers.

### Basic Usage

```python
from io import BytesIO
from rick.resource.stream import BytesIOSlice

# Create a memory buffer
buffer = BytesIO(b"Hello, World! This is a test.")

# Create a BytesIO slice
bytes_slice = BytesIOSlice(buffer)

# Get buffer size
print(f"Buffer size: {bytes_slice.size} bytes")

# Read entire buffer
data = bytes_slice.read()

# Read first 5 bytes
data = bytes_slice.read(offset=0, length=5)  # b"Hello"

# Read bytes 7-12
data = bytes_slice.read(offset=7, length=5)  # b"World"
```

### Constructor

**BytesIOSlice(buf: BytesIO)**

Creates a new BytesIOSlice instance.

**Parameters:**

- `buf` (BytesIO): BytesIO object to wrap

**Attributes:**

- `identifier`: The BytesIO object
- `size`: Buffer size in bytes

### Methods

**read(offset=0, length=-1) -> bytes**

Read data from the buffer.

**Parameters:**

- `offset` (int): Starting byte position (default: 0)
- `length` (int): Number of bytes to read (default: -1 for entire buffer)

**Returns:**

- `bytes`: Data read from buffer

## MultiPartReader

Combine multiple slices into a single seekable stream.

### Basic Usage

```python
from rick.resource.stream import FileSlice, BytesIOSlice, MultiPartReader
from io import BytesIO

# Create multiple parts
part1 = FileSlice('/path/to/file1.dat')
part2 = BytesIOSlice(BytesIO(b"Middle section"))
part3 = FileSlice('/path/to/file2.dat')

# Create multipart reader
reader = MultiPartReader(parts=[part1, part2, part3])

# Get total size
print(f"Total size: {reader.size} bytes")

# Read all data
for chunk in reader.read():
    process_chunk(chunk)

# Read specific range (bytes 100-200)
for chunk in reader.read(offset=100, length=100):
    process_chunk(chunk)
```

### Constructor

**MultiPartReader(parts: list = None)**

Creates a new MultiPartReader instance.

**Parameters:**

- `parts` (list): List of SliceReader objects (default: empty list)

**Attributes:**

- `parts`: List of SliceReader objects
- `size`: Total size of all parts combined
- `offset`: Current stream position (-1 if not opened)
- `opened`: Boolean indicating if stream has been read

### Methods

#### read(offset: int = None, length=-1)

Read data from the multipart stream as an iterator.

**Parameters:**

- `offset` (int): Starting byte position (default: current offset or 0)
- `length` (int): Number of bytes to read (default: -1 for all remaining)

**Returns:**

- Iterator yielding `bytes`: Chunks of data from the stream

**Raises:**

- `ValueError`: If offset is negative

**Example:**

```python
reader = MultiPartReader(parts=my_parts)

# Read entire stream
for chunk in reader.read():
    output.write(chunk)

# Read 1000 bytes starting at position 500
for chunk in reader.read(offset=500, length=1000):
    output.write(chunk)
```

#### seek(offset: int, whence: int = 0) -> int

Seek to a position in the stream.

**Parameters:**

- `offset` (int): Target byte position
- `whence` (int): Reference point (only SEEK_SET/0 is supported)

**Returns:**

- `int`: New position in stream

**Raises:**

- `ValueError`: If whence is not SEEK_SET or offset is negative

**Example:**

```python
reader = MultiPartReader(parts=my_parts)

# Seek to byte 1000
reader.seek(1000)

# Read from current position
for chunk in reader.read():
    process_chunk(chunk)
```

#### seekable() -> bool

Check if stream supports seeking.

**Returns:**

- `bool`: Always returns True

## Advanced Examples

### Combining Multiple Files

```python
from rick.resource.stream import FileSlice, MultiPartReader

# Create parts for multiple log files
parts = [
    FileSlice('/var/log/app.log.3'),
    FileSlice('/var/log/app.log.2'),
    FileSlice('/var/log/app.log.1'),
    FileSlice('/var/log/app.log'),
]

# Read all logs as single stream
reader = MultiPartReader(parts=parts)

with open('/tmp/combined.log', 'wb') as output:
    for chunk in reader.read():
        output.write(chunk)

print(f"Combined {len(parts)} files ({reader.size} bytes)")
```

### Streaming Upload

```python
from rick.resource.stream import FileSlice, BytesIOSlice, MultiPartReader
from io import BytesIO

# Build multipart upload with header, file, and footer
header = BytesIOSlice(BytesIO(b"--boundary\r\n"))
file_data = FileSlice('/path/to/upload.jpg')
footer = BytesIOSlice(BytesIO(b"\r\n--boundary--\r\n"))

reader = MultiPartReader(parts=[header, file_data, footer])

# Stream to server
for chunk in reader.read():
    upload_to_server(chunk)
```

### Partial File Processing

```python
from rick.resource.stream import FileSlice, MultiPartReader

# Process specific sections of large file
large_file = FileSlice('/data/largefile.bin')
reader = MultiPartReader(parts=[large_file])

# Process first megabyte
print("Processing header...")
for chunk in reader.read(offset=0, length=1024 * 1024):
    process_header(chunk)

# Seek to middle and process 1MB
middle = reader.size // 2
reader.seek(middle)
print("Processing middle section...")
for chunk in reader.read(offset=middle, length=1024 * 1024):
    process_data(chunk)

# Process last megabyte
end_offset = reader.size - (1024 * 1024)
reader.seek(end_offset)
print("Processing footer...")
for chunk in reader.read(offset=end_offset, length=1024 * 1024):
    process_footer(chunk)
```

### Custom Slice Implementation

```python
from rick.resource.stream import SliceReader, MultiPartReader


class DatabaseSlice(SliceReader):
    """Read data from database BLOB"""

    def __init__(self, db_connection, blob_id):
        # Get blob size from database
        size = db_connection.get_blob_size(blob_id)
        super().__init__(blob_id, size=size)
        self.db = db_connection

    def read(self, offset=0, length=-1):
        if length < 0:
            length = self.size
        # Read chunk from database
        return self.db.read_blob_chunk(
            self.identifier,
            offset,
            length
        )


# Use custom slice in MultiPartReader
blob1 = DatabaseSlice(db, 'blob_001')
blob2 = DatabaseSlice(db, 'blob_002')

reader = MultiPartReader(parts=[blob1, blob2])

# Stream database blobs as single file
with open('/tmp/output.dat', 'wb') as f:
    for chunk in reader.read():
        f.write(chunk)
```

### Memory-Efficient File Concatenation

```python
from rick.resource.stream import FileSlice, BytesIOSlice, MultiPartReader
from io import BytesIO

# Add separator between files
separator = BytesIOSlice(BytesIO(b"\n---\n"))

# Build parts list with separators
parts = []
files = ['/tmp/part1.txt', '/tmp/part2.txt', '/tmp/part3.txt']

for i, filepath in enumerate(files):
    parts.append(FileSlice(filepath))
    if i < len(files) - 1:
        parts.append(separator)

# Process as single stream without loading everything in memory
reader = MultiPartReader(parts=parts)

total_bytes = 0
with open('/tmp/combined.txt', 'wb') as output:
    for chunk in reader.read():
        output.write(chunk)
        total_bytes += len(chunk)

print(f"Concatenated {len(files)} files: {total_bytes} bytes")
```

### Range Request Handling

```python
from rick.resource.stream import FileSlice, MultiPartReader


def handle_range_request(file_path, range_start, range_end):
    """Handle HTTP range request efficiently"""

    file_slice = FileSlice(file_path)
    reader = MultiPartReader(parts=[file_slice])

    # Calculate length
    if range_end is None:
        range_end = reader.size - 1

    length = range_end - range_start + 1

    # Stream only requested range
    response_data = b''
    for chunk in reader.read(offset=range_start, length=length):
        response_data += chunk

    return response_data


# Example: Client requests bytes 1000-1999
data = handle_range_request('/videos/movie.mp4', 1000, 1999)
```

## Performance Considerations

### Memory Usage

MultiPartReader is designed for minimal memory usage:

```python
from rick.resource.stream import FileSlice, MultiPartReader

# These 3 files total 3GB, but we never load more than
# one chunk into memory at a time
parts = [
    FileSlice('/data/file1.bin'),  # 1GB
    FileSlice('/data/file2.bin'),  # 1GB
    FileSlice('/data/file3.bin'),  # 1GB
]

reader = MultiPartReader(parts=parts)

# Stream to destination with minimal memory footprint
with open('/data/combined.bin', 'wb') as output:
    for chunk in reader.read():
        output.write(chunk)
        # Each chunk is typically 8KB-64KB
        # Total memory usage stays constant
```

### Seeking Efficiency

Seeking is efficient as it calculates positions without reading data:

```python
from rick.resource.stream import FileSlice, MultiPartReader

parts = [FileSlice(f'/data/chunk{i}.bin') for i in range(100)]
reader = MultiPartReader(parts=parts)

# Seeking is O(n) where n is number of parts
# No data is read during seek
reader.seek(1024 * 1024 * 500)  # Seek to 500MB

# Only reads data from this point forward
for chunk in reader.read(length=1024):
    process_chunk(chunk)
```

### Buffering Strategy

For optimal performance with many small parts, consider buffering:

```python
from rick.resource.stream import BytesIOSlice, MultiPartReader
from io import BytesIO

# Instead of many small parts...
# BAD: many parts = many read() calls
parts_bad = [BytesIOSlice(BytesIO(b'x' * 10)) for _ in range(1000)]

# GOOD: combine small parts into larger buffers
buffer = BytesIO()
for i in range(1000):
    buffer.write(b'x' * 10)
buffer.seek(0)
parts_good = [BytesIOSlice(buffer)]

# Good approach has better performance
reader = MultiPartReader(parts=parts_good)
```

## Common Patterns

### Write Once, Read Many

```python
from rick.resource.stream import FileSlice, MultiPartReader

# Build multipart stream once
parts = [FileSlice(f) for f in my_files]
reader = MultiPartReader(parts=parts)

# Read multiple times with seeking
for iteration in range(3):
    reader.seek(0)  # Reset to beginning
    for chunk in reader.read():
        process_chunk(iteration, chunk)
```

### Chunked Processing

```python
from rick.resource.stream import FileSlice, MultiPartReader

CHUNK_SIZE = 1024 * 1024  # 1MB chunks

file_slice = FileSlice('/data/large.bin')
reader = MultiPartReader(parts=[file_slice])

offset = 0
while offset < reader.size:
    for chunk in reader.read(offset=offset, length=CHUNK_SIZE):
        process_chunk(chunk)
    offset += CHUNK_SIZE
```

## Error Handling

```python
from rick.resource.stream import FileSlice, MultiPartReader

try:
    # FileSlice validates file exists
    slice1 = FileSlice('/path/to/file.dat')
except ValueError as e:
    print(f"File error: {e}")

try:
    reader = MultiPartReader(parts=[slice1])

    # Negative offsets raise ValueError
    reader.seek(-100)
except ValueError as e:
    print(f"Seek error: {e}")

try:
    # Only SEEK_SET (0) is supported
    from io import SEEK_END

    reader.seek(0, SEEK_END)
except ValueError as e:
    print(f"Whence error: {e}")
```

## API Reference

### SliceReader

| Method                       | Description                                            |
|------------------------------|--------------------------------------------------------|
| `__init__(identifier, size)` | Initialize slice with identifier and size              |
| `read(offset, length)`       | Read data from slice (must be implemented by subclass) |

### FileSlice

| Method                 | Description                 |
|------------------------|-----------------------------|
| `__init__(file_path)`  | Create slice from file path |
| `read(offset, length)` | Read data from file         |

| Attribute    | Type | Description              |
|--------------|------|--------------------------|
| `identifier` | Path | Path object for the file |
| `size`       | int  | File size in bytes       |

### BytesIOSlice

| Method                 | Description                      |
|------------------------|----------------------------------|
| `__init__(buf)`        | Create slice from BytesIO buffer |
| `read(offset, length)` | Read data from buffer            |

| Attribute    | Type    | Description          |
|--------------|---------|----------------------|
| `identifier` | BytesIO | The BytesIO buffer   |
| `size`       | int     | Buffer size in bytes |

### MultiPartReader

| Method                 | Description                                  |
|------------------------|----------------------------------------------|
| `__init__(parts)`      | Create reader with list of SliceReader parts |
| `read(offset, length)` | Read data as iterator of chunks              |
| `seek(offset, whence)` | Seek to position (SEEK_SET only)             |
| `seekable()`           | Returns True (seeking is supported)          |

| Attribute | Type | Description                  |
|-----------|------|------------------------------|
| `parts`   | list | List of SliceReader objects  |
| `size`    | int  | Total size of all parts      |
| `offset`  | int  | Current stream position      |
| `opened`  | bool | Whether stream has been read |

## See Also

- [Resources Overview](index.md) - Overview of all resource utilities
- [Redis Cache](redis.md) - Redis caching with serialization
- [Configuration](config.md) - Configuration management
- [Serializers](../serializers/index.md) - Data serialization formats
