"""
RequestRecord with nested classes

Besides fields, RequestRecords can be initialized with other RequestRecord structures; this is useful to validate
complex/nested data or lists of records

- A record defines a nested structure of a given type;
- A recordset defines a list of structures of type;
"""
from rick.form import RequestRecord, field, recordset


class DeviceRequest(RequestRecord):
    fields = {
        'brand': field(validators="required|minlen:2|maxlen:128"),
        'model': field(validators="required|minlen:2|maxlen:128"),
        'ip_address': field(validators="required|ipv4"),
    }


class UserRequest(RequestRecord):
    fields = {
        'id': field(validators="numeric"),
        'name': field(validators="required|maxlen:128"),
        'age': field(validators="required|numeric|between:18,120"),

        # device is a DeviceRequesr record
        'devices': recordset(DeviceRequest, required=False)
    }


# create the request validation object to be used
req = UserRequest()

# ----------------------------------------------------------------------------
# valid data example
# ----------------------------------------------------------------------------
data = {
    'id': 12,
    'name': 'John Connor',
    'age': 30,
    'devices': [
        {
            'brand': 'Apple',
            'model': 'iPhone 6',
            'ip_address': '192.168.70.45',
        },
        {
            'brand': 'Apple',
            'model': 'iPad',
            'ip_address': '192.168.70.49',
        },
        {
            'brand': 'Huwawei',
            'model': 'P40',
            'ip_address': '192.168.70.12',
        }
    ]
}

# validate data, should be successful
if req.is_valid(data):
    print("data is valid, name is:", req.get('name'))
else:
    print(req.get_errors())

# ----------------------------------------------------------------------------
# invalid data, without devices
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
# invalid data, with devices
# ----------------------------------------------------------------------------
data = {
    'name': 'John Connor',
    'age': 12,
    'devices': [
        {
            'brand': 'Apple',
            'model': 'iPhone 6',
            'ip_address': '192.168.70.45',
        },
        {
            'brand': 'Apple',
            'model': 'iPad',
            'ip_address': '192.168.70.49',
        },
        {
            'brand': 'Huwawei',
            'model': 'P40',
            'ip_address': '192.168.70.12.5',  # Invalid IP
        }
    ]
}

# validate data, should fail
if req.is_valid(data):
    # this wont be shown, data is invalid
    print("data is valid, name is:", req.get('name'))
else:
    # will print:
    # {'devices': {'_': {2: {'ip_address': {'ipv4': 'invalid IPv4 address'}}}}, 'age': {'between': 'must be between 18 and 120'}}
    print(req.get_errors())
