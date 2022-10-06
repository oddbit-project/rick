"""
RequestRecord with custom field validator

RequestRecord classes can have additional custom validation methods; these are run *only* if the general request
validation rules pass; their purpose is to perform additional post-validation tasks, such as database lookups, etc

"""
from rick.form import RequestRecord, field
from rick.mixin import Translator


class UserRequest(RequestRecord):
    fields = {
        'id': field(validators="numeric"),
        'name': field(validators="required|maxlen:128"),
        'age': field(validators="required|numeric|between:18,120", error='invalid age')
    }

    # additional custom validator for field 'name'
    def validator_name(self, data, t: Translator):
        # this validator is only run if standard form validation is successful
        if data['name'] == 'T1000':
            # add a generic error to the field
            self.add_error('name', "I'll be back!")
            return False
        return True


# create the request validation object to be used
req = UserRequest()

# ----------------------------------------------------------------------------
# invalid data
# This won't trigger the custom validator yet
# ----------------------------------------------------------------------------
data = {
    'name': 'T1000',
    'age': 12
}

# validate data, should fail
if req.is_valid(data):
    # this wont be shown, data is invalid
    print("data is valid, name is:", req.get('name'))
else:
    # will print: {'age': {'*': 'invalid age'}}
    print(req.get_errors())

# ----------------------------------------------------------------------------
# invalid data
# This triggers the custom validator
# ----------------------------------------------------------------------------
data = {
    'name': 'T1000',
    'age': 19
}

# validate data, should fail
if req.is_valid(data):
    # this wont be shown, data is invalid
    print("data is valid, name is:", req.get('name'))
else:
    # data passes validation, but fails on the custom validator
    # will print: {'name': {'*': "I'll be back!"}}
    print(req.get_errors())
