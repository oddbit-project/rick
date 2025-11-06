# Console Output

Rick provides utilities for colored and formatted console output through the `AnsiColor` and `ConsoleWriter` classes.
These components make it easy to create visually appealing command-line interfaces with colored text, backgrounds, and
text attributes.

**Location:** `rick.resource.console`

## Overview

Console output utilities in Rick provide:

- **ANSI Color Support** - 16 foreground and background colors (standard and light variants)
- **Text Attributes** - Bold, dim, underline, and reversed text
- **High-Level Writer** - Pre-configured methods for common output types (success, error, warning, header)
- **Stream Control** - Separate stdout and stderr output
- **Flexible Styling** - Combine colors, backgrounds, and attributes

## Available Components

### AnsiColor

Low-level ANSI color formatting for text output.

**Location:** `rick.resource.console.AnsiColor`

### ConsoleWriter

High-level console writer with semantic output methods.

**Location:** `rick.resource.console.ConsoleWriter`

## AnsiColor

### Overview

`AnsiColor` provides dynamic color methods for all supported colors. Each color can be called as a method with optional
background color and text attributes.

### Supported Colors

**Foreground Colors:**

| Color   | Method      | Color         | Method            |
|---------|-------------|---------------|-------------------|
| Black   | `black()`   | Light Black   | `light_black()`   |
| Red     | `red()`     | Light Red     | `light_red()`     |
| Green   | `green()`   | Light Green   | `light_green()`   |
| Yellow  | `yellow()`  | Light Yellow  | `light_yellow()`  |
| Blue    | `blue()`    | Light Blue    | `light_blue()`    |
| Magenta | `magenta()` | Light Magenta | `light_magenta()` |
| Cyan    | `cyan()`    | Light Cyan    | `light_cyan()`    |
| White   | `white()`   | Light White   | `light_white()`   |

**Background Colors:**

All foreground colors can be used as background colors by passing them as the second parameter.

**Text Attributes:**

| Attribute   | Description                    |
|-------------|--------------------------------|
| `bold`      | Bold text                      |
| `dim`       | Dimmed text                    |
| `underline` | Underlined text                |
| `reversed`  | Reversed foreground/background |

### Basic Usage

```python
from rick.resource.console import AnsiColor

color = AnsiColor()

# Simple colored text
print(color.red('This is red text'))
print(color.green('This is green text'))
print(color.blue('This is blue text'))

# Light color variants
print(color.light_red('Light red text'))
print(color.light_green('Light green text'))
print(color.light_blue('Light blue text'))
```

### With Background Colors

```python
from rick.resource.console import AnsiColor

color = AnsiColor()

# Text with background color
print(color.red('Red text on white background', 'white'))
print(color.green('Green text on black background', 'black'))
print(color.yellow('Yellow text on blue background', 'blue'))

# Light backgrounds
print(color.black('Black text on light_yellow background', 'light_yellow'))
```

### With Text Attributes

```python
from rick.resource.console import AnsiColor

color = AnsiColor()

# Single attribute
print(color.red('Bold red text', attr='bold'))
print(color.blue('Underlined blue text', attr='underline'))
print(color.green('Dim green text', attr='dim'))

# Multiple attributes
print(color.yellow('Bold and underlined', attr=['bold', 'underline']))
print(color.magenta('Bold, dim, and underlined', attr=['bold', 'dim', 'underline']))
```

### Complete Styling

```python
from rick.resource.console import AnsiColor

color = AnsiColor()

# Combine color, background, and attributes
message = color.green(
    'SUCCESS: Operation completed',
    'white',
    ['bold', 'underline']
)
print(message)

# Build formatted output
error = color.red('ERROR:', attr='bold')
details = color.white('File not found: config.json')
print(f"{error} {details}")
```

### Method Signature

All color methods follow this signature:

```python
color.COLOR_NAME(message, bg_color=None, attr=None)
```

**Parameters:**

- `message` (str) - Text to colorize
- `bg_color` (str, optional) - Background color name
- `attr` (str or list, optional) - Single attribute or list of attributes

**Returns:** Formatted string with ANSI escape codes

### Color Combinations

```python
from rick.resource.console import AnsiColor

color = AnsiColor()

# Info message
info = color.blue('[INFO]', attr='bold')
print(f"{info} Application started")

# Success message
success = color.green('[SUCCESS]', attr='bold')
print(f"{success} Database connection established")

# Warning message
warning = color.yellow('[WARNING]', 'black', 'bold')
print(f"{warning} Low disk space")

# Error message
error = color.red('[ERROR]', attr=['bold', 'underline'])
print(f"{error} Failed to load configuration")
```

### Building Status Indicators

```python
from rick.resource.console import AnsiColor

color = AnsiColor()


def print_status(status, message):
    """Print status with color coding"""
    if status == 'success':
        icon = color.green('✓', attr='bold')
    elif status == 'error':
        icon = color.red('✗', attr='bold')
    elif status == 'warning':
        icon = color.yellow('!', attr='bold')
    else:
        icon = color.blue('i', attr='bold')

    print(f"{icon} {message}")


# Usage
print_status('success', 'All tests passed')
print_status('error', 'Connection failed')
print_status('warning', 'Deprecated API usage')
print_status('info', 'Loading configuration')
```

## ConsoleWriter

### Overview

`ConsoleWriter` provides a high-level interface for console output with pre-configured semantic methods for common
output types. It integrates with `AnsiColor` to provide colored output.

### Constructor

```python
ConsoleWriter(stdout=sys.stdout, stderr=sys.stderr, colorizer=AnsiColor())
```

**Parameters:**

- `stdout` - Output stream for standard output (default: `sys.stdout`)
- `stderr` - Output stream for error output (default: `sys.stderr`)
- `colorizer` - AnsiColor instance for colorization (default: new `AnsiColor()`)

### Methods

#### header(message, eol=True)

Write a header message in bold white.

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()
console.header('Application Configuration')
console.header('=' * 40)
```

#### success(message, eol=True)

Write a success message in green.

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()
console.success('Configuration loaded successfully')
console.success('Database connection established')
```

#### warn(message, eol=True)

Write a warning message in yellow.

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()
console.warn('Configuration file not found, using defaults')
console.warn('API rate limit approaching threshold')
```

#### error(message, eol=True)

Write an error message in red to stderr.

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()
console.error('Failed to connect to database')
console.error('Invalid configuration format')
```

#### write(message, eol=True)

Write a plain message to stdout.

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()
console.write('Starting application...')
console.write('Processing data...', eol=False)  # No newline
console.write(' Done')
```

#### write_error(message, eol=True)

Write a plain message to stderr.

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()
console.write_error('Critical: System resources low')
```

### Basic Usage

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()

# Application startup
console.header('My Application v1.0')
console.header('=' * 50)
console.write('')

# Status messages
console.write('Loading configuration...')
console.success('Configuration loaded')

console.write('Connecting to database...')
console.success('Database connection established')

# Warning
console.warn('Cache is disabled')

# Error
console.error('Failed to load plugin: analytics')
```

**Output:**

```
My Application v1.0  (bold white)
================================================== (bold white)

Loading configuration...
Configuration loaded  (green)
Connecting to database...
Database connection established  (green)
Cache is disabled  (yellow)
Failed to load plugin: analytics  (red, to stderr)
```

### Building CLI Applications

```python
import sys
from rick.resource.console import ConsoleWriter


def main():
    console = ConsoleWriter()

    console.header('Database Migration Tool')
    console.header('=' * 40)
    console.write('')

    # Step 1
    console.write('Step 1: Checking database connection...')
    try:
        check_database()
        console.success('  Database is accessible')
    except Exception as e:
        console.error(f'  Connection failed: {e}')
        return 1

    # Step 2
    console.write('Step 2: Running migrations...')
    try:
        run_migrations()
        console.success('  All migrations applied')
    except Exception as e:
        console.error(f'  Migration failed: {e}')
        return 1

    # Step 3
    console.write('Step 3: Verifying data integrity...')
    try:
        verify_data()
        console.success('  Data integrity verified')
    except Exception as e:
        console.warn(f'  Verification warning: {e}')

    console.write('')
    console.success('Migration completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

### Progress Indicators

```python
from rick.resource.console import ConsoleWriter
import time

console = ConsoleWriter()

tasks = [
    'Loading configuration',
    'Initializing database',
    'Starting services',
    'Running health checks'
]

for task in tasks:
    console.write(f'{task}...', eol=False)
    time.sleep(1)  # Simulate work
    console.success(' Done')

console.write('')
console.success('All tasks completed')
```

### Custom Output Streams

```python
from rick.resource.console import ConsoleWriter
from io import StringIO

# Capture output to strings
stdout_buffer = StringIO()
stderr_buffer = StringIO()

console = ConsoleWriter(stdout=stdout_buffer, stderr=stderr_buffer)

console.success('Success message')
console.error('Error message')

# Get captured output
stdout_content = stdout_buffer.getvalue()
stderr_content = stderr_buffer.getvalue()

print(f"Stdout: {stdout_content}")
print(f"Stderr: {stderr_content}")
```

### Integration with AnsiColor

```python
from rick.resource.console import ConsoleWriter, AnsiColor

color = AnsiColor()
console = ConsoleWriter(colorizer=color)

# Use ConsoleWriter for semantic messages
console.header('Processing Files')

# Use AnsiColor for custom styling
filename = color.cyan('config.json', attr='bold')
console.write(f'Reading {filename}')

status = color.green('OK', attr='bold')
console.write(f'Status: {status}')
```

## Advanced Usage

### Custom Console Class

```python
from rick.resource.console import ConsoleWriter, AnsiColor


class CustomConsole(ConsoleWriter):
    def info(self, message, eol=True):
        """Add info method"""
        formatted = self.colorizer.blue(f'[INFO] {message}')
        self.write(formatted, eol)

    def debug(self, message, eol=True):
        """Add debug method"""
        formatted = self.colorizer.light_black(f'[DEBUG] {message}')
        self.write(formatted, eol)

    def critical(self, message, eol=True):
        """Add critical method"""
        formatted = self.colorizer.red(f'[CRITICAL] {message}', attr='bold')
        self.write_error(formatted, eol)


# Usage
console = CustomConsole()
console.info('Application started')
console.debug('Loading configuration from /etc/app/config.json')
console.critical('System out of memory')
```

### Logging Integration

```python
from rick.resource.console import ConsoleWriter, AnsiColor
import logging


class ColoredConsoleHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.console = ConsoleWriter()

    def emit(self, record):
        msg = self.format(record)

        if record.levelno >= logging.ERROR:
            self.console.error(msg)
        elif record.levelno >= logging.WARNING:
            self.console.warn(msg)
        elif record.levelno >= logging.INFO:
            self.console.write(msg)
        else:  # DEBUG
            color = AnsiColor()
            self.console.write(color.light_black(msg))


# Setup logging
logger = logging.getLogger('myapp')
logger.addHandler(ColoredConsoleHandler())
logger.setLevel(logging.DEBUG)

# Use logger
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
```

### Table Output

```python
from rick.resource.console import ConsoleWriter, AnsiColor


def print_table(headers, rows):
    """Print a formatted table with colors"""
    console = ConsoleWriter()
    color = AnsiColor()

    # Print header
    header_text = ' | '.join(headers)
    console.header(header_text)
    console.header('-' * len(header_text))

    # Print rows
    for row in rows:
        # Color first column
        first = color.cyan(str(row[0]), attr='bold')
        rest = ' | '.join(str(cell) for cell in row[1:])
        console.write(f'{first} | {rest}')


# Usage
headers = ['ID', 'Name', 'Status', 'Count']
rows = [
    [1, 'Item A', 'Active', 100],
    [2, 'Item B', 'Inactive', 50],
    [3, 'Item C', 'Active', 75]
]

print_table(headers, rows)
```

### Progress Bar

```python
from rick.resource.console import ConsoleWriter, AnsiColor
import time


def progress_bar(total, console, color):
    """Simple progress bar"""
    bar_length = 40

    for i in range(total + 1):
        percent = i / total
        filled = int(bar_length * percent)
        bar = '█' * filled + '-' * (bar_length - filled)

        if percent < 0.5:
            bar_colored = color.red(bar)
        elif percent < 0.8:
            bar_colored = color.yellow(bar)
        else:
            bar_colored = color.green(bar)

        console.write(f'\r[{bar_colored}] {int(percent * 100)}%', eol=False)
        time.sleep(0.1)

    console.write('')  # New line


# Usage
console = ConsoleWriter()
color = AnsiColor()

console.header('Processing Files')
progress_bar(100, console, color)
console.success('Processing complete')
```

### Interactive Menu

```python
from rick.resource.console import ConsoleWriter, AnsiColor


def show_menu():
    """Display an interactive menu"""
    console = ConsoleWriter()
    color = AnsiColor()

    console.header('Main Menu')
    console.header('=' * 40)
    console.write('')

    options = [
        ('1', 'Start Application', 'green'),
        ('2', 'Stop Application', 'red'),
        ('3', 'View Logs', 'blue'),
        ('4', 'Configuration', 'yellow'),
        ('Q', 'Quit', 'white')
    ]

    for key, label, text_color in options:
        key_colored = color.cyan(f'[{key}]', attr='bold')
        label_colored = getattr(color, text_color)(label)
        console.write(f'  {key_colored} {label_colored}')

    console.write('')
    return input('Select option: ')


# Usage
choice = show_menu()
```

## Best Practices

### 1. Use Semantic Methods

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()

# Good: Use semantic methods
console.success('Operation completed')
console.error('Operation failed')
console.warn('Low memory')

# Less clear: Using write for everything
console.write('Operation completed')
console.write('Operation failed')
console.write('Low memory')
```

### 2. Consistent Color Scheme

```python
from rick.resource.console import AnsiColor

color = AnsiColor()

# Define consistent color scheme
STATUS_COLORS = {
    'active': 'green',
    'inactive': 'red',
    'pending': 'yellow',
    'unknown': 'light_black'
}


def colorize_status(status):
    color_name = STATUS_COLORS.get(status, 'white')
    return getattr(color, color_name)(status.upper(), attr='bold')


# Usage
print(f"Server status: {colorize_status('active')}")
```

### 3. Handle No-Color Environments

```python
import os
from rick.resource.console import ConsoleWriter, AnsiColor


def create_console():
    """Create console with color support detection"""
    # Check for NO_COLOR environment variable
    if os.getenv('NO_COLOR'):
        # Return console without colorization
        return PlainConsole()
    return ConsoleWriter()


class PlainConsole:
    """Console without colors for CI/CD environments"""

    def header(self, message, eol=True):
        print(message)

    def success(self, message, eol=True):
        print(f'[SUCCESS] {message}')

    def warn(self, message, eol=True):
        print(f'[WARNING] {message}')

    def error(self, message, eol=True):
        print(f'[ERROR] {message}')
```

### 4. Separate stdout and stderr

```python
from rick.resource.console import ConsoleWriter

console = ConsoleWriter()

# Good: Errors to stderr
console.error('Connection failed')

# Good: Normal output to stdout
console.write('Processing data...')
console.success('Processing complete')
```

### 5. Use eol Parameter for Dynamic Output

```python
from rick.resource.console import ConsoleWriter
import time

console = ConsoleWriter()

# Progress indicator
console.write('Loading', eol=False)
for i in range(5):
    console.write('.', eol=False)
    time.sleep(0.5)
console.write(' Done')
```

## Terminal Compatibility

ANSI color codes are supported on:

- **Linux/Unix** - Full support in all modern terminals
- **macOS** - Full support in Terminal.app and iTerm2
- **Windows 10+** - Full support in Windows Terminal and PowerShell
- **Windows (older)** - Limited support (may require ANSICON or colorama)

For maximum compatibility, consider using environment detection:

```python
import sys
import os


def supports_color():
    """Check if terminal supports ANSI colors"""
    # Check for NO_COLOR environment variable
    if os.getenv('NO_COLOR'):
        return False

    # Check if stdout is a TTY
    if not hasattr(sys.stdout, 'isatty'):
        return False

    if not sys.stdout.isatty():
        return False

    # Windows check
    if sys.platform == 'win32':
        return sys.version_info >= (3, 6)

    return True
```

## Related Topics

- [Configuration](config.md) - Use console output in configuration loaders
- [Forms](../forms/index.md) - Display form validation errors with colors
- [Validators](../validators/index.md) - Show validation results with formatting
