# rick
Python plumbing for micro-framework based applications

**Note**: This library is still under development; things may change place or be rewritten with a different spec between
releases.


## Documentation

Documentation is a work-in-progress. Please check what is available here: [Documentation](https://oddbit-project.github.io/rick/) 

Core components:
- Dependency Injection class;
- Resource loader (class factory);
- Class registry;
- Misc. Container classes;

Request components:
- Validator registry w/ [validators](https://oddbit-project.github.io/rick/validators/validator_list/);
- [Validation class](https://oddbit-project.github.io/rick/validators/);
- [Request validation](https://oddbit-project.github.io/rick/forms/requests/);
- [Forms](https://oddbit-project.github.io/rick/forms/);
- Filters;

Resource components:
- Configuration loader functions (environment, json);
- Console operation w/color;
- Cache facade w/ Redis support;

Misc components:
- Hasher; 
- Event Manager;
- Misc mixins;
- Extended json serializer;

