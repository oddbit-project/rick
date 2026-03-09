# Mixin rick.mixin.**Translator**

Mixin to provide an interface for string translation.

**Location:** `rick.mixin.Translator`

### Translator.**t(text: str) -> str:**

Method signature to perform a string translation. By default, the mixin implementation returns the passed *text* value.

Override this method to integrate with your application's localization system.

## Usage Example

```python
from rick.mixin import Translator


class GettextTranslator(Translator):
    """Translator implementation using gettext"""

    def __init__(self, translations):
        self._translations = translations

    def t(self, text: str) -> str:
        return self._translations.gettext(text)


# Use with forms
import gettext

lang = gettext.translation('messages', localedir='locales', languages=['pt'])
translator = GettextTranslator(lang)

# Pass to Form or RequestRecord
from rick.form import Form

form = Form(translator=translator)
# All field labels and error messages will be translated via gettext
form.field('text', 'name', 'Full Name', required=True)
```

The `Translator` mixin is used by [Form](../forms/form.class.md), [RequestRecord](../forms/requests.md), and [FieldSet](../forms/form.class.md#class-fieldset) to translate labels and error messages.
