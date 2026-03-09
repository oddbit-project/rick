# Class rick.form.**Field**

Base field class used by [Form](form.class.md) and [RequestRecord](requests.md) to define form fields
with validation, filtering, and metadata.

**Location:** `rick.form.Field`

## Constructor

### Field.**__init__(**kwargs)**

```python
Field(
    type="",
    label="",
    value=None,
    required=False,
    readonly=False,
    validators="",
    error=None,
    select=None,
    filter=None,
    attributes=None,
    options=None,
    bind=None,
)
```

**Parameters:**

| Parameter    | Type           | Default | Description                                                                 |
|--------------|----------------|---------|-----------------------------------------------------------------------------|
| `type`       | str            | `""`    | Field type (e.g. `'text'`, `'password'`, `'select'`)                        |
| `label`      | str            | `""`    | Display label                                                               |
| `value`      | Any            | `None`  | Predefined value                                                            |
| `required`   | bool           | `False` | If `True`, a `required` validator is prepended automatically                |
| `readonly`   | bool           | `False` | Mark field as read-only (also set via `options['readonly']`)                |
| `validators` | str or dict    | `""`    | Validator specification (pipe-separated string or dict)                     |
| `error`      | str or None    | `None`  | Custom error message for validation failures                                |
| `select`     | list           | `[]`    | List of allowed values for select-type fields                               |
| `filter`     | str or class   | `None`  | Filter name (e.g. `'int'`, `'datetime'`) or Filter subclass                |
| `attributes` | dict           | `{}`    | Optional visualization/HTML attributes                                      |
| `options`    | dict           | `{}`    | Extra field-specific options                                                |
| `bind`       | str or None    | `None`  | Alternate attribute name for data binding (used by `RequestRecord.bind()`)  |

### Validators Format

Validators can be specified as a pipe-separated string or a dict:

```python
# String format
Field(validators='required|email')
Field(validators='required|minlen:3|maxlen:50')

# Dict format
Field(validators={'required': None, 'minlen': 3, 'maxlen': 50})
```

See [Available Validators](../validators/validator_list.md) for the full list.

### Filter Usage

Filters transform the input value after validation:

```python
# By name (from the filter registry)
Field(filter='int')
Field(filter='datetime')

# By class
from rick.filter import Filter

class MyFilter(Filter):
    def transform(self, src):
        return src.strip().lower()

Field(filter=MyFilter)
```

See [Filters](../filters/index.md) for the full list.

## Attributes

After construction, the following attributes are available on the Field instance:

- `type` (str) - Field type
- `label` (str) - Display label
- `value` - Current value (set after validation)
- `required` (bool) - Whether the field is required
- `readonly` (bool) - Whether the field is read-only
- `validators` (str or dict) - Validator specification
- `error_message` (str or None) - Custom error message
- `select` (list) - Select options
- `filter` (Filter or None) - Filter instance
- `attributes` (dict) - Visualization attributes
- `options` (dict) - Extra options
- `bind` (str or None) - Binding name

## Helper Functions

Rick provides helper functions for declaring fields as specifications (used with class-based
`RequestRecord` definitions).

### field(**kwargs) -> dict

Create a field specification dictionary. Accepts the same keyword arguments as the `Field` constructor.

```python
from rick.form import RequestRecord, field

class UserRequest(RequestRecord):
    fields = {
        'name': field(validators='required|minlen:2'),
        'email': field(validators='required|email'),
        'age': field(validators='int', filter='int'),
    }
```

### record(cls, required=False, error=None) -> dict

Create a specification for a nested record (dict-like sub-form). The `cls` must be a
`RequestRecord` subclass.

```python
from rick.form import RequestRecord, field, record

class AddressRequest(RequestRecord):
    fields = {
        'street': field(validators='required'),
        'city': field(validators='required'),
    }

class UserRequest(RequestRecord):
    fields = {
        'name': field(validators='required'),
        'address': record(AddressRequest, required=True),
    }
```

### recordset(cls, required=False, error=None) -> dict

Create a specification for a list of nested records. The `cls` must be a `RequestRecord` subclass.

```python
from rick.form import RequestRecord, field, recordset

class ItemRequest(RequestRecord):
    fields = {
        'product_id': field(validators='required|id'),
        'quantity': field(validators='required|int'),
    }

class OrderRequest(RequestRecord):
    fields = {
        'customer_id': field(validators='required|id'),
        'items': recordset(ItemRequest, required=True),
    }
```

## Related Topics

- [Form Class](form.class.md) - Full-featured form with fieldsets and controls
- [RequestRecord](requests.md) - Request validation with field management
- [Validators](../validators/validator_list.md) - Available validation rules
- [Filters](../filters/index.md) - Available input filters
