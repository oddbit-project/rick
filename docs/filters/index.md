# Filters

Filter classes are helper classes used to transform a specific source value (tipically a string) into a specific data type, such as
a string into a datetime object. The lifecycle of filter class objects is usually managed via a Registry, but many
contexts that accept a filter name will also accept a custom filter class.

These classes don't perform any validation of the passed values; if the conversion operation fails, they will silently
return None. 

## Using filters

While Filters are often use within the scope of a Form, FieldRecord or RequestRecord, they can also be used in standalone:
```python
from datetime import datetime
from rick.filter import registry as filter_registry

# retrieve a filter to convert a string to a datetime object
filter = filter_registry.get('datetime')

# use the filter to convert the string to an object
result = filter.transform('2022-05-31T15:11Z')

# console output: True
print(isinstance(result, datetime))
```

## Creating Filters

Filter classes must extend the Filter base class, and implement the appropriate behaviour in the overridden transform() method:

```python
from datetime import datetime
from rick.filter import registry as filter_registry, Filter
from typing import Any
from dataclasses import dataclass

# our new Dude type
@dataclass
class Dude:
    greeting: str

# add our new filter to registry, with the name 'dude'
@filter_registry.register_cls('dude')
class DudeFilter(Filter):

    def transform(self, src: Any) -> Dude:
        # all values are now dude objects!
        return Dude(greeting="Hey dude!")


# retrieve a filter to convert a string to a "dude"
filter = filter_registry.get('dude')

# use the filter to convert the string to a dude
result = filter.transform('the quick brown fox jumps over the lazy dog')

# console output: "Hey Dude!"
print(result.greeting)
```

