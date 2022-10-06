"""
RequestRecord with nested classes

Besides fields, RequestRecords can be initialized with other RequestRecord structures; this is useful to validate
complex/nested data or lists of records

- A record defines a nested structure of a given type;
- A recordset defines a list of structures of type;
"""
from rick.form import RequestRecord, field, record


class AddressRequest(RequestRecord):
    fields = {
        'street': field(validators="required|minlen:4"),
        'city': field(validators="required|minlen:2"),
        'country': field(validators="required|minlen:2"),
    }


class UserRequest(RequestRecord):
    fields = {
        'id': field(validators="numeric"),
        'name': field(validators="required|maxlen:128"),
        'age': field(validators="required|numeric|between:18,120"),

        # address is a AddressRequest record
        'address': record(AddressRequest, required=False)
    }


# create the request validation object to be used
req = UserRequest()

# ----------------------------------------------------------------------------
# valid data example
# ----------------------------------------------------------------------------
data = {
    'id': 12,
    'name': 'John Connor',
    'age': 30
}

# validate data, should be successful
if req.is_valid(data):
    print("data is valid, name is:", req.get('name'))
else:
    print(req.get_errors())

# ----------------------------------------------------------------------------
# invalid data, without address
# ----------------------------------------------------------------------------
data = {
    'name': 'John Connor',
    'age': 12
}

# validate data, should fail
if req.is_valid(data):
    # this wont be shown, data is invalid
    print("data is valid, name is:", req.get('name'))
else:
    # will print: {'age': {'between': 'must be between 18 and 120'}}
    print(req.get_errors())

# ----------------------------------------------------------------------------
# invalid data, with address
# ----------------------------------------------------------------------------
data = {
    'name': 'John Connor',
    'age': 12,
    'address': {
        'street': None,
        'city': 'Berlin',
        'country': 'Germany'
    }
}

# validate data, should fail
if req.is_valid(data):
    # this wont be shown, data is invalid
    print("data is valid, name is:", req.get('name'))
else:
    # will print:
    # {'address': {'_': {'street': {'required': 'value required'}}}, 'age': {'between': 'must be between 18 and 120'}}
    print(req.get_errors())
