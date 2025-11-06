# Rick Validator Examples

This directory contains examples demonstrating the Rick validator module.

## Simple Example

The `simple_example.py` demonstrates basic validator usage:

```python
from rick.validator import Validator

# Create validator with rules
validator = Validator()
validator.add_field('email', 'required|email')
validator.add_field('age', 'required|numeric|between:18,120')

# Validate data
data = {'email': 'user@example.com', 'age': '25'}
if validator.is_valid(data):
    print("Data is valid!")
else:
    print(f"Errors: {validator.get_errors()}")
```

## Running the Examples

```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/rick:$PYTHONPATH

# Run the simple example
python examples/validator/simple_example.py
```

## Available Rules

### String Rules
- `required` - Field must be present and not empty
- `alpha` - Only alphabetic characters
- `alphanum` - Only alphanumeric characters
- `slug` - URL-safe slug (lowercase, hyphens, underscores)
- `minlen:N` - Minimum length of N characters
- `maxlen:N` - Maximum length of N characters
- `len:N` or `len:min,max` - Exact or range length

### Numeric Rules
- `numeric` - Must be a number
- `int` - Must be an integer
- `decimal` - Must be a decimal number
- `between:min,max` - Must be between min and max

### Network Rules
- `email` - Valid email address
- `ipv4` - Valid IPv4 address
- `ipv6` - Valid IPv6 address
- `ip` - Valid IPv4 or IPv6 address
- `fqdn` - Fully qualified domain name
- `mac` - Valid MAC address

### Hash Rules
- `md5` - Valid MD5 hash
- `sha1` - Valid SHA-1 hash
- `sha256` - Valid SHA-256 hash
- `sha512` - Valid SHA-512 hash

### Other Rules
- `bool` - Boolean value
- `uuid` - Valid UUID
- `iso8601` - Valid ISO 8601 date/time
- `in:val1,val2` - Value must be in list
- `notin:val1,val2` - Value must not be in list

## Rule Formats

### String Format (Laravel-style)
```python
validator.add_field('email', 'required|email')
validator.add_field('age', 'numeric|between:18,120')
```

### Dictionary Format
```python
validator.add_field('email', {
    'required': None,
    'email': None
})
validator.add_field('age', {
    'numeric': None,
    'between': [18, 120]
})
```

## Custom Error Messages

```python
validator.add_field('email', 'email', "Please provide a valid email")
```

## Validation API

### `add_field(field_name, rules, error_message=None)`
Add a field to validate with its rules.

### `is_valid(data) -> bool`
Validate data dictionary. Returns True if valid, False if errors.

### `get_errors(field_name=None) -> dict`
Get all validation errors or errors for a specific field.

### `reset()`
Clear all validation errors (useful for re-validating).

### `clear()`
Clear all validation rules.

## Common Patterns

### User Registration
```python
validator = Validator()
validator.add_field('username', 'required|alphanum|minlen:3')
validator.add_field('email', 'required|email')
validator.add_field('password', 'required|minlen:8')
validator.add_field('age', 'numeric|between:13,120')  # Optional

if validator.is_valid(form_data):
    # Register user
    pass
else:
    # Show errors
    errors = validator.get_errors()
```

### Optional Fields
Fields without the `required` rule are optional:
```python
validator.add_field('email', 'email')  # Optional but must be valid if provided
validator.add_field('website', 'fqdn')  # Optional
```

### Multiple Validators
```python
# Email validator
email_validator = Validator()
email_validator.add_field('email', 'required|email')

# Password validator
password_validator = Validator()
password_validator.add_field('password', 'required|minlen:8')
```

## Documentation

For complete documentation, see:
- [Validators Overview](../../docs/validators/index.md)
- [Available Validators](../../docs/validators/validator_list.md)

## Support

- **Issues**: https://github.com/oddbit-project/rick/issues
- **Documentation**: https://oddbit-project.github.io/rick/
- **Repository**: https://github.com/oddbit-project/rick
