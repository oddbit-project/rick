import os
import pytest
from rick.resource.config import EnvironmentConfig
from rick.base import ShallowContainer


class ConfigTest1(EnvironmentConfig):
    OPTION_1 = None
    OPTION_2 = 'x'


class ConfigTest2(EnvironmentConfig):
    FOO_LIST = []
    FOO_INT = 1
    FOO_STR = None
    FOO_DICT = {}


fixture_configtest1 = [(ConfigTest1, {'OPTION_1': 'abc', 'OPTION_2': 'def'})]
fixture_configtest_prefix = [(ConfigTest1, {'PREFIX_OPTION_1': 'abc', 'PREFIX_OPTION_2': 'def'})]

fixture_configtest2 = [(
    ConfigTest2,
    {  # env vars
        'FOO_LIST': 'abc,def',
        'FOO_INT': '5',
        'FOO_STR': 'joe',
        'FOO_DICT': '{"key":"value"}'
    },  # expected result
    {
        'foo_list': ['abc', 'def'],
        'foo_int': 5,
        'foo_str': 'joe',
        'foo_dict': {"key": "value"}
    }
)]


@pytest.mark.parametrize("fixture", fixture_configtest1)
def test_EnvConfig(fixture):
    for name, value in fixture[1].items():
        os.environ[name] = str(value)

    # build config object
    cfg = fixture[0]().build()

    # check if values were overridden
    for name, value in fixture[1].items():
        assert cfg.get(name.lower()) == str(value)


@pytest.mark.parametrize("fixture", fixture_configtest_prefix)
def test_EnvConfig_prefix(fixture):
    for name, value in fixture[1].items():
        os.environ[name] = str(value)

    # build config object
    prefix = 'PREFIX_'
    cfg = fixture[0]().build(prefix)

    # check if values were overridden
    for name, value in fixture[1].items():
        assert cfg.get(name.replace(prefix, '').lower()) == str(value)


@pytest.mark.parametrize("fixture", fixture_configtest2)
def test_EnvConfig_types(fixture):
    obj = fixture[0]()

    # first, check that build() processes correctly without any set env variables
    cfg = obj.build()
    for name in dir(obj):
        if name.isupper():
            value = cfg.get(name.lower())
            if isinstance(value, ShallowContainer):
                # unrap dict from ShallowContainer
                value = value.asdict()
            assert value == getattr(obj, name)

    # now set env variables
    for name, value in fixture[1].items():
        os.environ[name] = str(value)

    # re-build cfg with overriden values
    cfg = obj.build()
    # verify overriden values match expected values
    for name, value in fixture[1].items():
        value = cfg.get(name.lower())
        if isinstance(value, ShallowContainer):
            value = value.asdict()
        assert value == fixture[2][name.lower()]
