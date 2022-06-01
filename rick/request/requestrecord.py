from typing import Any, List
from rick.mixin import Translator
from rick.validator import Validator
from rick.form import Field
import inspect

class RequestRecord:
    _errors = {}

    def clear(self):
        """
        :return: self
        """
        self._errors = {}
        return self

    def is_valid(self, data: dict, t: Translator = None) -> bool:
        """
        Validate fields
        :param data: dict of values to validate
        :param t: Optional translator mixin
        :return: True if dict is valid, False otherwise
        """
        self._errors = {}
        if t is None:
            t = Translator()
        validator = Validator()
        field_names = []
        for field_name in dir(self):
            field = getattr(self, field_name)
            if isinstance(field, Field):
                field_names.append(field_name)
                if len(field.validators) > 0:
                    validator.add_field(field_name, field.validators, field.messages)

        if validator.is_valid(data, t):
            # set values for fields
            for field_name in field_names:
                field = getattr(self, field_name, None)
                # attempt to find a method called validator_<field_id>() in the current object
                method_name = "_".join(['validator', field_name.replace('-', '_')])
                custom_validator = getattr(self, method_name, None)
                # if exists and is method
                if custom_validator and callable(custom_validator):
                    # execute custom validator method
                    if not custom_validator(data, field, t):
                        # note: errors are added inside the custom validator method
                        return False

                if field_name in data.keys():
                    if field.filter is None:
                        field.value = data[field_name]
                    else:
                        field.value = field.filter.transform(data[field_name])
                else:
                    field.value = None
            return True

        self._errors = validator.get_errors()
        return False

    def get_errors(self) -> dict:
        """
        Get validation errors
        :return:
        """
        return self._errors

    def clear_errors(self):
        """
        Clean the error collection
        :return: none
        """
        self._errors = {}

    def add_error(self, id: str, error_message: str, t: Translator=None):
        """
        Adds or overrides a validation error to a field
        if field already have errors, they are removed and replaced by a wildcard error
        :param id field id
        :param error_message error message
        :param t: optional Translator object
        :return self
        """
        field = getattr(self, id, None)
        if not isinstance(field, Field):
            raise ValueError("invalid field id %s" % (id,))

        if t is not None:
            error_message = t.t(error_message)

        self._errors[id] = {'*': error_message}
        return self

    def get(self, id: str) -> Any:
        """
        Retrieve field value by id
        :param id: field id
        :return: Any
        """
        field = getattr(self, id, None)
        if isinstance(field, Field):
           return field.value
        return None

    def get_data(self) -> dict:
        """
        Retrieve all data as a dict
        :return: dict
        """
        result = {}
        for field_name in dir(self):
            if not field_name.startswith('_'):
                f = getattr(self, field_name, None)
                if isinstance(f, Field):
                    result[field_name] = f.value
        return result

    def set(self, id: str, value: Any):
        """
        Set field value
        :param id: field id
        :param value: value
        :return: self
        """
        field = getattr(self, id, None)
        if isinstance(field, Field):
            field.value = value
        return self
