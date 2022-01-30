from typing import Any
from rick.mixin import Translator
from rick.validator import Validator


class Field:
    type = ""
    label = ""
    value = None
    required = False
    validators = ""
    messages = None
    select = []
    attributes = {}
    options = {}

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self.required:
            # add required validator
            if len(self.validators) == 0:
                self.validators = {'required': None}
            else:
                if isinstance(self.validators, str):
                    self.validators = self.validators + "|required"
                elif isinstance(self.validators, dict):
                    self.validators['required'] = None


class FieldSet:

    def __init__(self, id: str, label: str):
        self.id = id
        self.label = label
        self.form = None
        self.fields = {}

    def use_form(self, form: object):
        """
        Set parent form object
        :param form:
        :return:
        """
        self.form = form

    def field(self, field_type: str, field_id: str, label: str, **kwargs):
        """
        Adds a field

        Optional kwargs:
        value=None: Field value
        required=True: If field is required
        validators=[list] |  validators="string": Validator list
        messages={}: Custom validation messages
        select=[list]: dict of values for select
        attributes={}: optional visualization attributes
        options={}: optional field-specific options

        :param field_type:
        :param field_id:
        :param label:
        :return: self
        """

        if field_id in self.fields.keys():
            raise RuntimeError("duplicated field id '%s'" % (id,))

        kwargs['type'] = field_type
        kwargs['label'] = label
        field = Field(**kwargs)
        self.fields[field_id] = field
        self.form.add_field(field_id, field)
        return self


class Form:
    DEFAULT_FIELDSET = '__default__'

    def __init__(self, translator: Translator = None):
        self._fieldset = {}
        self.fields = {}
        self.validator = Validator()
        self._translator = translator
        self.fieldset(self.DEFAULT_FIELDSET, '')

    def fieldset(self, id: str, label: str) -> FieldSet:
        """
        Adds/retrieves a fieldset to the form
        If fieldset doesn't exist, it is created
        :param id: fieldset id
        :param label: fieldset legend
        :return: FieldSet
        """
        # if its existing, just return it
        if id in self._fieldset.keys():
            return self._fieldset[id]

        fs = FieldSet(id, label)
        fs.use_form(self)
        self._fieldset[id] = fs
        return fs

    def field(self, field_type: str, field_id: str, label: str, **kwargs):
        """
        Adds a field to the form

        Alias for FieldSet:field(), and will use the internal DEFAULT_FIELDSET

        :param field_type:
        :param field_id:
        :param label:
        :param kwargs:
        :return:
        """
        return self.fieldset(self.DEFAULT_FIELDSET, '').field(field_type, field_id, label, **kwargs)

    def add_field(self, id: str, field: Field):
        """
        Add a field object to the internal collection
        :param id: field id
        :param field: field object
        :return: self
        """
        self.fields[id] = field
        self.validator.add_field(id, field.validators, field.messages)
        return self

    def is_valid(self, data: dict) -> bool:
        """
        Validate fields
        :param data: dict of values to validate
        :return: True if dict is valid, False otherwise
        """
        if self.validator.is_valid(data, self._translator):
            # set values for fields
            for id, field in self.fields.items():
                if id in data.keys():
                    field.value = data[id]
                else:
                    field.value = None
            return True
        return False

    def error_messages(self) -> dict:
        """
        Get validation error messages
        :return: dict
        """
        return self.validator.get_errors()

    def get(self, id: str) -> Any:
        """
        Retrieve field value by id
        :param id: field id
        :return: Any
        """
        if id in self.fields.keys():
            return self.fields[id].value
        return None

    def set(self, id: str, value: Any):
        """
        Set field value
        :param id: field id
        :param value: value
        :return: self
        """
        if id in self.fields.keys():
            self.fields[id].value = value
        return self
