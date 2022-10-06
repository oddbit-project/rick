"""
Simple RequestRecord example
"""
from rick.form import RequestRecord, field


class UserRequest(RequestRecord):
    fields = {
        'id': field(validators="numeric"),
        'name': field(validators="required|maxlen:128"),
        'age': field(validators="required|numeric|between:18,120")
    }

# create the request validation object to be used
req = UserRequest()

#----------------------------------------------------------------------------
# valid data example
#----------------------------------------------------------------------------
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


#----------------------------------------------------------------------------
# invalid data
#----------------------------------------------------------------------------
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
