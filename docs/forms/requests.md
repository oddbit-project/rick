# Managing Requests

Rick provides several distinct classes to aid the management of request data: **RequestRecord** and [Form](index.md). While these
classes share a common syntax, their use cases are different. RequestRecord is designed to just handle structured request
data; Form extends RequestRecord with additional control and grouping logic, useful for generating and processing HTML forms.

## RequestRecord

RequestRecord provides two ways for defining fields and field-related validation and filtering operations; A terse
version, suitable for most usage scenarios, where the fields are specified directly in the class declaration (via *fields* 
attribute), or in runtime by using an initializer method, often called init().

Declaring fields directly using class attributes:
```python
from rick.form import RequestRecord, field

class UserRequest(RequestRecord):
    fields = {
        'id': field(validators="numeric"),
        'name': field(validators="required|maxlen:128"),
        'age': field(validators="required|numeric|between:18,120")
    }
```

Declaring fields inside an initializer method:
```python
from rick.form import RequestRecord
from rick.mixin import Translator

# Custom class using runtime field definitions, and a custom field validator
class UserRequest(RequestRecord):
    
    def init(self):
        self.field('id', validators="required|minlen:4|maxlen:8") \
            .field('age', validators="required|numeric|between:9,125") \
            .field('phone',validators="numeric|minlen:8|maxlen:16")
        return self
```

## RequestRecord validation

There are two levels of validation: a first one, using the declared validators, and a second one using optional methods
to perform additional validation.

Validation of data is done by using RequestRecord's is_valid() method. This method receives a dictionary of field names
and values, and returns either True or False, reflecting if all the values for the defined fields pass the predefined
validators or not, as well as the optional validation methods.

> **Note:** internally, the validation is performed as a **two-step operation** - if any of the declared field validators fail
> validation, no magic validation methods are called.
> Magic validation methods will only be executed for any given field if **all** the predefined field validations pass.
>
> The rationale for this is to avoid having to perform basic validations within the method body, simplifying the implementation
> of additional validation logic. This way, when any magic method is called, it is **guaranteed** that the available data
> passed the field validations.


### Field validators

field validators can be specified using any format compatible with [rick.Validator](../validators/index.md) usage, but commonly will use the
string Laravel-style compact form:

```python
from rick.form import RequestRecord, field

class AgeRequest(RequestRecord):
    fields = {
        # age field with several validators
        'age': field(validators="required|numeric|between:18,120")
    }

# create the request validation object to be used
req = AgeRequest()

# some invalid data to fail validation
data = {
    'name': 'John Connor',
    'age': '1a'
}

# validate data, should fail
if not req.is_valid(data):
    # will print: 
    # {'age': {'numeric': 'only digits allowed', 'between': 'must be between 18 and 120'}}
    print(req.get_errors())
```

Each failing validator will generate an error message; it is possible to override all error messages for a given field
by just providing a custom error message:


```python
from rick.form import RequestRecord, field

class AgeRequest(RequestRecord):
    fields = {
        # age field with several validators
        'age': field(validators="required|numeric|between:18,120", error="invalid age")
    }

# create the request validation object to be used
req = AgeRequest()

# some invalid data to fail validation
data = {
    'name': 'John Connor',
    'age': '1a'
}

# validate data, should fail
if not req.is_valid(data):
    # will print: 
    # {'age': {'*': 'invalid age'}}
    print(req.get_errors())
```

### Method validators

As mentioned, RequestRecord allows for the optional declaration of magic validation methods that are called automatically
during the internal second validation step. These methods can be used to perform additional validation logic, such as
dependencies between fields or database lookups.

The methods must be named *validator_<fieldname>(data, t:Translator)* and conform to the defined interface:
```python
from rick.form import RequestRecord, field
from rick.mixin import Translator

# Custom class using runtime field definitions, and a custom field validator
class MyFieldRecord(RequestRecord):
    fields = {
        'name': field(validators="required|minlen:4|maxlen:8"),
        'age': field(validators="required|numeric|between:9,125"),
        'phone': field(validators="numeric|minlen:8|maxlen:16")
    }

    # custom validator method for field 'name'
    # this will only be executed if all field validators are successful
    def validator_name(self, data, t:Translator):
        # 'data' is the field:value dictionary passed to is_valid(); it
        # contains all raw field values
        if data['name'] == 'dave':
            # add a custom error for field 'name'
            self.add_error('name', 'Dave is not here, man')
            return False
        return True

data = {
    'name': 'dave',
    'age': 12,
    'phone': '12312312'
}

frm = MyFieldRecord()
if not  frm.is_valid(data):
    # will print:
    # {'name': {'*': 'Dave is not here, man'}}
    print(frm.get_errors())
```


### Retrieving validation errors

Validation errors are made available via *get_errors()*, using the [documented format](errors.md).


## Nested RequestRecord structures

RequestRecord classes can be nested to build complex request validation structures. This can be achieved using the
**record()** helper function to describe dict-like records, or **recordset()** helper function to describe lists
of dict-like records.

Internally, records are also represented as fields, so filtered values can be accessed like any other regular field.

Example:
```python
from rick.form import RequestRecord, field, record, recordset
from rick.mixin import Translator

# Request class describing a player structure
class Player(RequestRecord):
    fields = {
        'name': field(validators="required|minlen:4|maxlen:32"),
        'age': field(validators="required|numeric|between:9,125"),
    }

# Request class for a team
class TeamRequest(RequestRecord):
    fields = {
        'team_name': field(validators="required|minlen:4|maxlen:64"),
        # specify a field 'players' as a list of type Player, for validation purposes
        'players': recordset(Player)
    }
    
# Request class for a team leader
class TeamLeaderRequest(RequestRecord):
    fields = {
        'team_name': field(validators="required|minlen:4|maxlen:64"),
        # specify a field 'players' as a single record of type Player, for validation purposes
        'leader': record(Player)
    }
    
# sample request data for TeamRequest    
team_data = {
    'team_name': 'super team',
    'players': [
        {
            'name': 'susan',
            'age': 32
        },
        {
            'name': 'mary',
            'age': 21
        },
    ]
}
    
# validate data for TeamRequest
request = TeamRequest()
if request.is_valid(team_data):
    print('Team data is valid!')

# sample request data for TeamLeaderRequest    
team_leader_data = {
    'team_name': 'super team',
    'leader': {
            'name': 'susan',
            'age': 32
        }
}
    
# validate data for TeamLeaderRequest
request = TeamLeaderRequest()
if request.is_valid(team_leader_data):
    print('Team leader data is valid!')
```

