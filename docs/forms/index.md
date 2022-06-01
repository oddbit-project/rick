# Working with Forms

[rick.Form](form.class.md#Form) is a generic Form component to aid the maintenance of a form or request lifecycle. 
It supports the declaration of fields, field groups (fieldsets) and perform validation on those fields, including custom validation. Due to its
agnostic nature, it does not provide any form rendering mechanism.




## Custom Validation

It is possible to perform additional custom validation on a given field to be executed automatically - just add a method
with the name **validate_<field_id>(data, field: Field)** to your class, where *data* will be the dict with the received
values to validate, and field is the current field object for the specified field. 

**Note:** The custom validator methods are only executed if the initial validation of the form is valid (after all the
specified field validators on the field definition are run and validated **True**); If the form isn't valid, these methods
are not executed.

Custom validation method example:

```python
from rick.form import Form, Field


class ExampleForm(Form):

    def init(self):
        self.field('text', 'name', 'Name', validators="required|minlen:4|maxlen:8")
        return self

    def validator_name(self, data, field: Field):
        # this validator is only run if standard form validation is successful
        if data['name'] == 'Dave':
            self.add_error('name', 'Dave is not here, man')
            return False
        return True


frm = ExampleForm().init()

# trigger a failure on the field validators
# the additional existing validator method for field 'name' won't be called 
valid = frm.is_valid({'name': 'Teo'})
print(valid, frm.get_errors())

# trigger a failure on the validation method
# the field validators executed without errors
valid = frm.is_valid({'name': 'Dave'})
print(valid, frm.get_errors())

# Console output:
# False {'name': {'minlen': 'minimum allowed length is 4'}}
# False {'name': {'*': 'Dave is not here, man'}}
#
```


