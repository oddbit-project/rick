# Managing Requests

Rick provides several distinct classes to aid the management of request data: FieldRecord, RequestRecord and Form. While these
classes share a common syntax, their use cases are different.

## FieldRecord

The FieldRecord class implements common form field handling. The fields are defined dynamically, allowing for the
adding or removal of fields in runtime. It has no additional control logic available, nor provides a way of grouping
fields.

FieldRecord example:
```python
from rick.form import FieldRecord
from rick.mixin import Translator

class MyFieldRecord(FieldRecord):

    def init(self):
        self.field('name', validators="required|minlen:4|maxlen:8") \
            .field('age', validators="required|numeric|between:9,125") \
            .field('phone',validators="numeric|minlen:8|maxlen:16")
        return self

    def validator_name(self, data, t:Translator):
        """
        Sample custom validator for field 'name'
        This validator is triggered during the is_valid() call when the all the initial field validators execute
        successfully 
        """
        if data['name'] == 'dave':
            self.add_error('name', 'Dave is not here, man')
            return False
        return True

(...)

data = {}

frm = MyFieldRecord().init()
if frm.is_valid(data):
    pass
    # do something on success
else:
    # dump error string
    print(frm.get_errors())
```

## Form

The Form class extends FieldRecord and adds grouping of fields (fieldsets), support for control elements (buttons, etc)
and basic HTTP-related properties, such as action URL and HTTP method.

Form example:
```python
from rick.form import Form
from rick.mixin import Translator

class MyForm(Form):

    def init(self):
        self.set_action('/user/create')
        self.set_method(self.METHOD_POST)
        
        # implicitly uses the default fieldset
        self.field('text', 'name', 'Full Name', validators="required|minlen:4|maxlen:8") \
            .field('text', 'age', 'Age', validators="required|numeric|between:9,125") \
            .field('text', 'phone', 'Phone', validators="numeric|minlen:8|maxlen:16")

        # a separate fieldset
        self.fieldset('tab2', 'Details')\
            .field('text', 'address', 'Home Address', validators="required")
        
        self.control('submit', 'save', 'Save') \
            .control('reset', 'clear', 'Clear Form')
        return self

    def validator_name(self, data, t:Translator):
        """
        Sample custom validator for field 'name'
        This validator is triggered during the is_valid() call when the all the initial field validators execute
        successfully 
        """
        if data['name'] == 'dave':
            self.add_error('name', 'Dave is not here, man')
            return False
        return True


(...)

data = {}

frm = MyForm().init()
if frm.is_valid(data):
    pass
    # do something on success
else:
    # dump error string
    print(frm.get_errors())
```

## RequestRecord

The RequestRecord class provides a way of declaring and validating simple field structures, suitable for eg. API usage.
Fields are defined on class declaration, and there is no field grouping available, nor an initializer method.
All the field-related options are available, including validators and filters. On success, field values can be accessed
directly via the attributes, e.g. object.field.value.

Please note: field names must **not** start with an underscore('_'); underscore attributes are considered private and internal
to the class implementation.

RequestRecord example:

```python
from rick.form import Field
from rick.request import RequestRecord
from rick.mixin import Translator

class UserRequest(RequestRecord):
    name = Field(validators="required|minlen:4|maxlen:8")
    age = Field(validators="required|numeric|between:9,125")
    phone = Field(validators="numeric|minlen:8|maxlen:16")
    
    def validator_name(self, data, t:Translator):
        """
        Sample custom validator for field 'name'
        This validator is triggered during the is_valid() call when the all the initial field validators execute
        successfully 
        """
        if data['name'] == 'dave':
            self.add_error('name', 'Dave is not here, man')
            return False
        return True


(...)

data = {}

frm = UserRequest()
if frm.is_valid(data):
    print("User name is: {}".format(frm.name.value))
else:
    # dump error string
    print(frm.get_errors())
```
