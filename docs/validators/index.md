# Validators

Rick validators is a registry-based reusable approach to validation operations. It implements a programmatic approach
of validating a dictionary of fields and values against a predefined validation specification. This specification can either 
be in dictionary format (suitable when specs are read from external sources, such as JSON), or in compact format, a
string-based format based on PHP Laravel's validator specification, suitable for inline or programmatic usage.

## TL;DR; Example

```python
from rick.validator import Validator

# a compact spec example
spec_compact = {
    'field1': 'required|maxlen:3',  # field is required, maximum length is 3
    'field2': 'minlen:4', # field is optional, minimum length is 4
    'field3': 'required|numeric|len:2,4' # field is required, must be digits, with a length between 2 and 4
}

# a dict spec example
spec_dict = {
    'field1': {
        'required': None,
        'maxlen': 3,
    },
    'field2': {
        'minlen': 4,
    },
    'field3': {
        'required': None,
        'numeric': None,
        'len': [2, 4],
    }
}

# field data dict to perform validation on
fields_values = {
    'field1': 'abc',
    'field2': 'def',
    'field3': 12345
}

# validate compact notation
v = Validator(spec_compact)
# perform validation, should return False with errors in field2 and field3
valid = v.is_valid(fields_values)
#
# console output:
# False {'field2': {'minlen': 'minimum allowed length is 4'}, 'field3': {'len': 'length must be between [2, 4]'}}
print(valid, v.get_errors())


# validate with dict notation
v = Validator(spec_dict)
# perform validation, should return False with errors in field2 and field3
valid = v.is_valid(fields_values)
#
# console output:
# False {'field2': {'minlen': 'minimum allowed length is 4'}, 'field3': {'len': 'length must be between [2, 4]'}}
print(valid, v.get_errors())

# retrieve errors for specific fields
#
# console output: {'minlen': 'minimum allowed length is 4'}
print(v.get_errors('field2'))
#
# console output: {'len': 'length must be between [2, 4]'}
print(v.get_errors('field3'))


# Simulate optional field - remove field2 from value dictionary
# the validation result should fail, but without any error for field2, because its absent
fields_values.pop('field2')
valid = v.is_valid(fields_values)
#
# console output:
# False {'field3': {'len': 'length must be between [2, 4]'}}
print(valid, v.get_errors())
```

## Specification: Dict format

The dict format spectification is a 2-level dictionary, where the first level keys are field names, and the second level
keys are validator names and optional parameters.

Example of a dict format specification with 2 validators, one of them (**len**) with validator parameters:
```python
spec = {
  'field_name': {
      'required': None,
      'len':[2,4]
  }
}
```

## Specification: Compact format

The compact format specification is a string with one or several validator names concatenated with '|'. Some validators require one
or more parameters; these are specified as a comma-separared list after a ':' following the validator name.

Example of a compact format specification with 2 validators, one of them (**len**) with validator parameters:
```python
spec = {
  'field_name': 'required|len:2,4'
}
```

## Available validators

The complete list of available validators is available [here](validator_list.md).


## Optional fields and aborting on first fail



## Chaining validators


## Validator Class


## Adding custom Validators
