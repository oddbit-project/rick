# Rick Form Examples

This directory contains examples demonstrating the Rick form module for building and validating forms.

## Overview

The Rick form module provides powerful form handling capabilities:

- **Form** - HTML-style forms with fieldsets and controls
- **RequestRecord** - Lightweight request validation for APIs
- **Field** - Individual field definitions with validation
- **Validators** - Built-in validation rules
- **Custom validation** - Define custom validator methods
- **Data binding** - Bind form data to Python objects

## Examples

### simple_form.py

Basic form usage examples:

- Creating simple forms
- Adding fields with validation
- Validating form data
- Accessing field values
- Setting values programmatically
- Handling validation errors

**Run:**
```bash
python examples/form/simple_form.py
```

**Key concepts:**
- `Form()` - Create a form instance
- `form.field()` - Add fields with validators
- `form.is_valid(data)` - Validate data
- `form.get(field_id)` - Get field value
- `form.get_data()` - Get all field values
- `form.set(field_id, value)` - Set field value

### custom_validation.py

Custom validation examples:

- Custom validator methods
- Password confirmation validation
- Age verification
- Prohibited usernames
- Date range validation
- Manual error handling
- Complex business logic

**Run:**
```bash
python examples/form/custom_validation.py
```

**Key concepts:**
- `validator_<field_name>()` - Custom validation methods
- `form.add_error()` - Manually add errors
- Multi-field validation
- Business rule enforcement

### fieldset_example.py

Fieldset organization examples:

- Creating fieldsets to group fields
- Multiple fieldsets in a single form
- Employee registration with categories
- Survey forms
- Accessing fieldset information

**Run:**
```bash
python examples/form/fieldset_example.py
```

**Key concepts:**
- `form.fieldset(id, label)` - Create/retrieve fieldset
- `fieldset.field()` - Add field to fieldset
- `form.get_fieldsets()` - Get all fieldsets
- Organizing complex forms

### request_record_example.py

RequestRecord for API validation:

- Simple request records
- Nested records
- Recordsets (lists of records)
- Binding to Python objects
- Custom field name binding
- API request validation

**Run:**
```bash
python examples/form/request_record_example.py
```

**Key concepts:**
- `RequestRecord` - Base class for request validation
- `field()` - Field specification helper
- `record()` - Nested record specification
- `recordset()` - List of records specification
- `record.bind(Class)` - Bind to object
- `record.bindx(Class)` - Bind with unmapped values

## Common Patterns

### Basic Form Validation

```python
from rick.form import Form

form = Form()
form.field("text", "username", "Username", validators="required|alphanum")
form.field("email", "email", "Email", validators="required|email")

data = {"username": "alice", "email": "alice@example.com"}

if form.is_valid(data):
    print("Valid!")
    print(f"Username: {form.get('username')}")
else:
    print(f"Errors: {form.get_errors()}")
```

### Custom Validation

```python
from rick.form import Form
from rick.mixin import Translator

class MyForm(Form):
    def __init__(self):
        super().__init__()
        self.field("password", "password", "Password", validators="required")
        self.field("password", "confirm", "Confirm", validators="required")

    def validator_confirm(self, data, t: Translator):
        if data['password'] != data['confirm']:
            self.add_error('confirm', 'Passwords do not match')
            return False
        return True
```

### RequestRecord with Binding

```python
from rick.form import RequestRecord, field

class UserRequest(RequestRecord):
    fields = {
        'username': field(validators='required|alphanum'),
        'email': field(validators='required|email'),
    }

class User:
    username = None
    email = None

record = UserRequest()
data = {'username': 'alice', 'email': 'alice@example.com'}

if record.is_valid(data):
    user = record.bind(User)
    print(f"User: {user.username}")
```

### Nested Records

```python
from rick.form import RequestRecord, field, record

class AddressRecord(RequestRecord):
    fields = {
        'city': field(validators='required'),
        'state': field(validators='required'),
    }

class PersonRecord(RequestRecord):
    fields = {
        'name': field(validators='required'),
        'address': record(AddressRecord, required=True),
    }

data = {
    'name': 'John',
    'address': {'city': 'NYC', 'state': 'NY'}
}

person = PersonRecord()
if person.is_valid(data):
    print("Valid nested data!")
```

## Available Validators

Rick supports many built-in validators:

### String Validators
- `required` - Field must be present and not empty
- `alpha` - Only alphabetic characters
- `alphanum` - Only alphanumeric characters
- `minlen:N` - Minimum length
- `maxlen:N` - Maximum length
- `len:min,max` - Length range

### Numeric Validators
- `numeric` - Must be numeric
- `int` - Must be integer
- `decimal` - Must be decimal
- `between:min,max` - Value range

### Network Validators
- `email` - Valid email address
- `ipv4` - Valid IPv4 address
- `ipv6` - Valid IPv6 address
- `fqdn` - Fully qualified domain name
- `mac` - Valid MAC address

### Other Validators
- `uuid` - Valid UUID
- `iso8601` - Valid ISO 8601 date/time
- `bool` - Boolean value
- `dict` - Dictionary value
- `list` - List value

## Form Methods

### Form

| Method | Description |
|--------|-------------|
| `field(type, id, label, **kwargs)` | Add a field to the form |
| `fieldset(id, label)` | Create/retrieve a fieldset |
| `control(type, id, label, **kwargs)` | Add a control element |
| `is_valid(data)` | Validate form data |
| `get(field_id)` | Get field value |
| `set(field_id, value)` | Set field value |
| `get_data()` | Get all field values as dict |
| `get_errors()` | Get validation errors |
| `add_error(field_id, message)` | Manually add error |
| `set_action(url)` | Set form action URL |
| `set_method(method)` | Set HTTP method |

### RequestRecord

| Method | Description |
|--------|-------------|
| `is_valid(data)` | Validate request data |
| `get(field_id)` | Get field value |
| `set(field_id, value)` | Set field value |
| `get_data()` | Get all values as dict |
| `bind(Class)` | Bind data to object |
| `bindx(Class)` | Bind with unmapped values |
| `get_errors()` | Get validation errors |
| `add_error(field_id, message)` | Manually add error |

## Field Parameters

When adding fields, you can specify:

- `type` - Field type (text, email, password, etc.)
- `label` - Field label
- `validators` - Validation rules (string or dict)
- `required` - If field is required (bool)
- `value` - Default value
- `error` - Custom error message
- `select` - List of options for select fields
- `attributes` - HTML attributes (dict)
- `options` - Additional options (dict)
- `bind` - Custom bind name for object binding

## See Also

- [Forms Documentation](../../docs/forms/) - Complete form documentation
- [Validators Documentation](../../docs/validators/) - Validator reference
- [Rick Documentation](https://oddbit-project.github.io/rick/) - Full documentation

## Support

- **Issues**: https://github.com/oddbit-project/rick/issues
- **Documentation**: https://oddbit-project.github.io/rick/
- **Repository**: https://github.com/oddbit-project/rick
