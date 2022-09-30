import json
import os
from rick.base import ShallowContainer
from typing import Any, List

class EnvironmentConfig:
    """
    Base class for environment-based config

    Config attributes must be named uppercase; These attribute names will be translated to lowercase
    on the ShallowContainer; The uppercase names are used to override values from existing environment variables

    Example:
        EXISTING OS ENV VARS: [DB_NAME="some_db", DB_HOST="abc"]

        class MyConfig(EnvironmentConfig):
            DB_NAME = 'mydb'
            DB_HOST = 'localhost'
            DB_USERNAME = 'username'
            DB_PASSWORD = 'password'

        cfg = MyConfig().build()
        assert cfg['db_name'] == 'some_db'
        assert cfg['db_host'] == 'abc'
        assert cfg['db_username'] == 'abc'
    """
    list_separator = ','

    def build(self, prefix='') -> ShallowContainer:
        """
        Assemble a final ShallowContainer based on the env vars
        Note: The env vars also override the object values
        :param prefix: optional prefix name for env vars
        :return: ShallowContainer
        """
        data = {}
        for name in dir(self):
            if name.isupper():
                value = getattr(self, name)
                if not callable(value):
                    value = self._parse_value(prefix + name, value)
                    setattr(self, name, value)
                    data[name.lower()] = value
        return ShallowContainer(data)

    def _parse_value(self, env_var_name, existing_value) -> Any:
        """
        Simple mapper to extract environment variables based on type

        :param env_var_name: env var to process
        :param existing_value: existing default value
        :return: overridden value of correct existing_value type, if env var exists; existing_value otherwise
        """
        value = os.environ.get(env_var_name)
        if value is None:
            return existing_value

        # if default value of attribute is none, always assume string
        if existing_value is None:
            return value

        mapper = getattr(self, "_{}_conv".format(type(existing_value).__name__))
        if not mapper:
            raise ValueError("Invalid data type detected when parsing environment variable '{}'".format(env_var_name))
        return mapper(value)

    def _str_conv(self, v) -> str:
        """
        String mapper
        :param v:
        :return: str
        """
        return str(v)

    def _int_conv(self, v) -> int:
        """
        Int mapper
        :param v:
        :return: int
        """
        return int(v)

    def _list_conv(self, v) -> List:
        """
        List mapper
        :param v: a string containing multiple string values, separated by self.list_separator
        :return: List
        """
        if not type(v) is str:
            raise ValueError("Invalid data type to extract list: expecting str, got '{}'".format(type(v).__name__))
        return str(v).split(self.list_separator)

    def _dict_conv(self, v) -> dict:
        """
        Dict mapper
        :param v: a json string containing an object (dict)
        :return: dict
        """
        if not type(v) is str:
            raise ValueError("Invalid data type to extract dict: expecting str, got '{}'".format(type(v).__name__))
        try:
            return json.loads(v)
        except e:
            raise ValueError("Error when parsing JSON: {}".format(e))
