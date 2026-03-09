# Class rick.form.**Form**

Full-featured form class with fieldset and control support. Extends [RequestRecord](requests.md) with
HTML form concepts such as actions, methods, fieldsets, and controls.

**Location:** `rick.form.Form`

## Constants

| Constant           | Value      | Description            |
|--------------------|------------|------------------------|
| `DEFAULT_FIELDSET` | `__default__` | Default fieldset id |
| `METHOD_POST`      | `POST`     | HTTP POST method       |
| `METHOD_PUT`       | `PUT`      | HTTP PUT method        |
| `METHOD_PATCH`     | `PATCH`    | HTTP PATCH method      |
| `METHOD_SEARCH`    | `SEARCH`   | HTTP SEARCH method     |

## Constructor

### Form.**__init__(translator: Translator = None)**

Initializes the form. Optionally receives a [Translator](../mixins/translator.class.md) mixin to
provide translation services to all fields and fieldsets.

```python
from rick.form import Form

# Basic form
form = Form()

# Form with translator
form = Form(translator=my_translator)
```

## Properties

### @property Form.**fields**

Form field dictionary, indexed by field id. Each entry is a [Field](field.class.md) object.

## Methods

### Form.**set_action(url: str) -> self**

Set the form action URL.

```python
form.set_action('/api/users')
```

### Form.**get_action() -> str**

Get the current action URL.

```python
url = form.get_action()
```

### Form.**set_method(method: str) -> self**

Set the HTTP method for the form.

```python
form.set_method(Form.METHOD_PUT)
```

### Form.**get_method() -> str**

Get the current HTTP method.

```python
method = form.get_method()  # "POST"
```

### Form.**clear()**

Remove all fields, fieldsets, controls, and reset method and action to defaults.

```python
form.clear()
```

### Form.**fieldset(id: str, label: str) -> FieldSet**

Add or retrieve a fieldset. If the fieldset doesn't exist, it is created. If it already exists,
its label is updated (unless label is empty).

```python
# Create a fieldset
fs = form.fieldset('personal', 'Personal Information')

# Add fields to it
fs.field('text', 'name', 'Full Name', required=True)
fs.field('text', 'email', 'Email', validators='required|email')
```

**Parameters:**

- `id` (str) - Fieldset identifier
- `label` (str) - Fieldset legend/label (translated automatically)

**Returns:** `FieldSet` instance

### Form.**field(field_type: str, field_id: str, label: str, **kwargs) -> FieldSet**

Add a field to the default fieldset. This is an alias for `fieldset(DEFAULT_FIELDSET, "").field(...)`.

```python
form.field('text', 'username', 'Username', required=True)
form.field('password', 'password', 'Password', validators='required|minlen:8')
```

**Parameters:**

- `field_type` (str) - Field type (e.g. `'text'`, `'password'`, `'select'`)
- `field_id` (str) - Unique field identifier
- `label` (str) - Field label (translated automatically)
- `**kwargs` - Additional parameters passed to [Field](field.class.md) constructor

### Form.**control(control_type: str, control_id: str, label: str, **kwargs) -> self**

Add a control element (e.g. submit button) to the form.

```python
form.control('submit', 'btn_save', 'Save')
form.control('button', 'btn_cancel', 'Cancel', attributes={'class': 'secondary'})
```

**Parameters:**

- `control_type` (str) - Control type
- `control_id` (str) - Unique control identifier
- `label` (str) - Control label (translated automatically)
- `**kwargs` - Additional attributes passed to `Control` constructor

### Form.**add_field(id: str, field: Field) -> self**

Add a Field object directly to the internal collection and register its validators.

**Parameters:**

- `id` (str) - Field identifier
- `field` (Field) - Field object

### Form.**add_error(id: str, error_message: str) -> self**

Add or override a validation error for a field. The error message is translated if a
translator is available.

```python
if username_taken:
    form.add_error('username', 'Username already in use')
```

**Parameters:**

- `id` (str) - Field identifier (must exist)
- `error_message` (str) - Error message

**Raises:** `ValueError` if field id does not exist

### Form.**get_fieldsets() -> dict**

Get the internal fieldset dictionary.

```python
fieldsets = form.get_fieldsets()
for fs_id, fs in fieldsets.items():
    print(fs.id, fs.label)
```

**Returns:** dict of `{id: FieldSet}`

## Class **FieldSet**

A fieldset groups related fields under a common label.

### FieldSet.**__init__(parent: RequestRecord, id: str, label: str)**

**Attributes:**

- `id` (str) - Fieldset identifier
- `label` (str) - Fieldset label
- `fields` (dict) - Dictionary of fields in this fieldset

### FieldSet.**field(field_type: str, field_id: str, label: str, **kwargs) -> self**

Add a field to the fieldset. The field is also registered on the parent form.

**Parameters:**

- `field_type` (str) - Field type
- `field_id` (str) - Unique field identifier
- `label` (str) - Field label (translated automatically)
- `**kwargs` - Additional parameters passed to [Field](field.class.md) constructor (value, required, validators, select, attributes, options, etc.)

## Class **Control**

A simple container for form control elements (buttons, etc.).

**Attributes:**

- `type` (str) - Control type
- `label` (str) - Control label
- `value` - Control value
- `attributes` (dict) - HTML attributes
- `options` (dict) - Extra options

## Complete Example

```python
from rick.form import Form

class UserForm(Form):
    def __init__(self):
        super().__init__()
        self.set_action('/users')
        self.set_method(Form.METHOD_POST)

        # Personal information fieldset
        personal = self.fieldset('personal', 'Personal Info')
        personal.field('text', 'first_name', 'First Name', required=True)
        personal.field('text', 'last_name', 'Last Name', required=True)
        personal.field('text', 'email', 'Email', validators='required|email')

        # Account fieldset
        account = self.fieldset('account', 'Account Settings')
        account.field('password', 'password', 'Password', validators='required|minlen:8')
        account.field('select', 'role', 'Role', select=['user', 'admin'])

        # Controls
        self.control('submit', 'save', 'Save')
        self.control('button', 'cancel', 'Cancel')


form = UserForm()
if form.is_valid(request_data):
    data = form.get_data()
else:
    errors = form.get_errors()
```

## Related Topics

- [Field Class](field.class.md) - Field definition and constructor parameters
- [RequestRecord](requests.md) - Parent class with validation and data binding
- [Validators](../validators/index.md) - Available validation rules
- [Filters](../filters/index.md) - Input transformation filters
