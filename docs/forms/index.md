# Working with Forms

Rick provides powerful form handling and request validation capabilities through two main classes:

- **[Form](form.class.md#Form)** - Full-featured forms with fieldsets, controls, and HTML form support
- **[RequestRecord](requests.md)** - Lightweight request validation for APIs and data processing

## Overview

### Form

Form is a generic form component designed for building and validating HTML forms. It supports:

- Field declaration with validation rules
- Field groups (fieldsets) for organizing complex forms
- Custom validation methods
- Form controls (buttons, etc.)
- HTTP method and action URL configuration
- Agnostic design (no rendering - bring your own template engine)

### RequestRecord

RequestRecord is a lightweight class focused on structured request data validation. It's ideal for:

- API request validation
- Data processing pipelines
- Nested data structures
- Object binding
- Microservices and REST APIs

## Quick Start

### Simple Form

```python
from rick.form import Form

# Create form
form = Form()
form.field("text", "username", "Username", validators="required|alphanum|minlen:3")
form.field("email", "email", "Email", validators="required|email")
form.field("password", "password", "Password", validators="required|minlen:8")

# Validate data
data = {
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123"
}

if form.is_valid(data):
    print(f"Welcome {form.get('username')}!")
else:
    print(f"Errors: {form.get_errors()}")
```

### Simple RequestRecord

```python
from rick.form import RequestRecord, field


class UserRequest(RequestRecord):
    fields = {
        'username': field(validators='required|alphanum|minlen:3'),
        'email': field(validators='required|email'),
        'age': field(validators='numeric|between:18,120'),
    }


# Validate request data
request = UserRequest()
data = {'username': 'alice', 'email': 'alice@example.com', 'age': '25'}

if request.is_valid(data):
    print("Valid request!")
    user_data = request.get_data()
```

## Form Features

### Adding Fields

```python
form = Form()

# Basic field
form.field("text", "name", "Full Name", validators="required")

# Field with multiple validators
form.field("text", "age", "Age", validators="required|numeric|between:18,120")

# Optional field (no 'required' validator)
form.field("text", "phone", "Phone", validators="numeric")
```

### Using Fieldsets

```python
form = Form()

# Personal information fieldset
personal = form.fieldset("personal", "Personal Information")
personal.field("text", "first_name", "First Name", validators="required")
personal.field("text", "last_name", "Last Name", validators="required")

# Contact information fieldset
contact = form.fieldset("contact", "Contact Information")
contact.field("email", "email", "Email", validators="required|email")
contact.field("text", "phone", "Phone", validators="numeric")
```

### Adding Controls

```python
form = Form()
form.field("text", "username", "Username", validators="required")
form.field("password", "password", "Password", validators="required")

# Add form controls (buttons)
form.control("submit", "login", "Login")
form.control("button", "cancel", "Cancel")
```

### Form Configuration

```python
form = Form()
form.set_action("/api/users")
form.set_method(Form.METHOD_POST)

# Available methods:
# - Form.METHOD_POST
# - Form.METHOD_PUT
# - Form.METHOD_PATCH
# - Form.METHOD_SEARCH
```

## Custom Validation

Custom validator methods are executed automatically after standard field validation passes. The method name must follow
the pattern `validator_<field_id>()`.

**Note:** Custom validators only run if all field validators pass first. This ensures you don't need to repeat basic
validation logic in your custom methods.

### Basic Custom Validation

```python
from rick.form import Form
from rick.mixin import Translator


class RegistrationForm(Form):
    def __init__(self):
        super().__init__()
        self.field('text', 'username', 'Username', validators="required|alphanum")
        self.field('password', 'password', 'Password', validators="required|minlen:8")
        self.field('password', 'confirm', 'Confirm Password', validators="required")

    def validator_confirm(self, data, t: Translator):
        """Validate password confirmation"""
        if data['password'] != data['confirm']:
            self.add_error('confirm', 'Passwords do not match')
            return False
        return True

    def validator_username(self, data, t: Translator):
        """Check if username is available"""
        # Simulate database check
        taken_usernames = ['admin', 'root', 'system']
        if data['username'].lower() in taken_usernames:
            self.add_error('username', 'Username not available')
            return False
        return True
```

### Multi-Field Validation

```python
from rick.form import Form
from rick.mixin import Translator


class DateRangeForm(Form):
    def __init__(self):
        super().__init__()
        self.field('date', 'start_date', 'Start Date', validators="required")
        self.field('date', 'end_date', 'End Date', validators="required")

    def validator_end_date(self, data, t: Translator):
        """Ensure end date is after start date"""
        start = data.get('start_date', '')
        end = data.get('end_date', '')

        if start and end and end < start:
            self.add_error('end_date', 'End date must be after start date')
            return False
        return True
```

## Working with Form Data

### Getting Field Values

```python
form = Form()
form.field("text", "name", "Name", validators="required")
form.field("email", "email", "Email", validators="required|email")

data = {"name": "Alice", "email": "alice@example.com"}

if form.is_valid(data):
    # Get individual field
    name = form.get('name')

    # Get all data as dict
    all_data = form.get_data()
```

### Setting Field Values

```python
form = Form()
form.field("text", "name", "Name")
form.field("email", "email", "Email")

# Set values programmatically
form.set("name", "Bob")
form.set("email", "bob@example.com")

print(form.get('name'))  # Output: Bob
```

## Validation Errors

After validation fails, retrieve errors using `get_errors()`:

```python
form = Form()
form.field("text", "username", "Username", validators="required|minlen:3")
form.field("email", "email", "Email", validators="required|email")

data = {"username": "ab", "email": "invalid"}

if not form.is_valid(data):
    errors = form.get_errors()
    # {
    #   'username': {'minlen': 'minimum allowed length is 3'},
    #   'email': {'email': 'invalid email address'}
    # }
```

See [Error Format Documentation](errors.md) for complete error structure details.

## Available Validators

Rick includes many built-in validators. Common validators include:

**String Validators:**

- `required` - Field must be present and not empty
- `alpha` - Alphabetic characters only
- `alphanum` - Alphanumeric characters only
- `minlen:N` - Minimum length
- `maxlen:N` - Maximum length

**Numeric Validators:**

- `numeric` - Must be numeric
- `int` - Must be integer
- `decimal` - Must be decimal
- `between:min,max` - Value range

**Network Validators:**

- `email` - Valid email address
- `ipv4` / `ipv6` - IP addresses
- `fqdn` - Fully qualified domain name

See the [Validators Documentation](../validators/index.md) for the complete list.

## Examples

Rick includes comprehensive form examples in `examples/form/`:

- **simple_form.py** - Basic form usage
- **custom_validation.py** - Custom validators and business logic
- **fieldset_example.py** - Organizing forms with fieldsets
- **request_record_example.py** - API validation and nested records

Run examples:

```bash
python examples/form/simple_form.py
```

## See Also

- [Form Class Reference](form.class.md) - Complete Form API
- [Field Class Reference](field.class.md) - Field options and parameters
- [RequestRecord Documentation](requests.md) - API request validation
- [Error Format](errors.md) - Error message structure
- [Validators](../validators/index.md) - Available validation rules


