# RequestRecord/Form error messages

RequestRecord and form error messages have the following structure:

```
{
  field_name: {
    validator_name: error_message,
    validator_name: error_message
  },
  field-name: {...}
}
```
Where field_name is the field id, and validator_name either the name of the failing validator, or '*' for
generic error messages for the field.


Example result, with two failing validations on a single field:
```json
 {
  "age": {
    "between": "must be between 9 and 125",
    "numeric": "only digits allowed"
  }
}
```

## Nested Records

Nested record errors are signaled by using '_' as validator name. The nested record can either be a single record, or a
list of records:

Structure for single record:
```
{
  field_name: {
    validator_name: error_message,
    validator_name: error_message
  },
  field-name: {
    validator_name: error_message,
    "_": {
        field_name: {
            validator_name: error_message,
            validator_name: error_message,
        },
        field_name: {
            validator_name: error_message,
            validator_name: error_message,
        },
    }
  }
}
```


Structure for a list of records (notice the sequence number to identify the failing record position):
```
{
  field_name: {
    validator_name: error_message,
    validator_name: error_message
  },
  field-name: {
    validator_name: error_message,
    "_": {
        "sequence number": {
            field_name: {
                validator_name: error_message,
                validator_name: error_message,
            },
            field_name: {
                validator_name: error_message,
                validator_name: error_message,
            },
        }
    }
  }
}
```