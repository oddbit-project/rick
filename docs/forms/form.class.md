# Class rick.form.**Form**

Base form class.

### @property Form.**fields**

Form field dictionary, indexed by field id. Each entry is a [Field](field.class.md#field) object. 

### Form.**__init__(translator: Translator = None)**

Form Constructor. Initializes the form object, and optionally receives a [Translator](../mixins/translator.class.md#translator) mixin to
provide translation services to all the fields and fieldsets.

