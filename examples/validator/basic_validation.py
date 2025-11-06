"""
Basic validator usage examples

This example demonstrates:
- Creating validators
- Validating data
- Accessing validation results
- Handling errors
"""

from rick.validator import Validator


def simple_validation():
    """Simple field validation"""
    print("=== Simple Field Validation ===")

    # Define validation rules using string format
    validator = Validator()
    validator.add_field('email', 'email')
    validator.add_field('age', 'numeric')

    # Valid data
    data = {
        'email': 'user@example.com',
        'age': '25'
    }

    is_valid = validator.is_valid(data)
    print(f"Valid data: {data}")
    print(f"Validation passed: {is_valid}")
    print(f"Errors: {validator.get_errors() if not is_valid else 'None'}")
    print()

    # Invalid data
    invalid_data = {
        'email': 'invalid-email',
        'age': 'not-a-number'
    }

    is_valid = validator.is_valid(invalid_data)
    print(f"Invalid data: {invalid_data}")
    print(f"Validation passed: {is_valid}")
    print(f"Errors: {validator.get_errors()}")
    print()


def required_fields():
    """Validating required fields"""
    print("=== Required Fields ===")

    validator = Validator()
    validator.add_field('username', 'required')
    validator.add_field('email', 'required|email')
    validator.add_field('password', 'required|minlen:8')

    # Complete data
    data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'SecurePass123'
    }

    is_valid = validator.is_valid(data)
    print(f"Complete data - Valid: {is_valid}")
    print(f"Data: {data}")
    print()

    # Missing fields
    incomplete_data = {
        'username': 'bob'
        # email and password missing
    }

    is_valid = validator.is_valid(incomplete_data)
    print(f"Incomplete data - Valid: {is_valid}")
    print(f"Errors: {validator.get_errors()}")
    print()


def multiple_rules():
    """Applying multiple rules to a field"""
    print("=== Multiple Rules Per Field ===")

    validator = Validator()
    validator.add_field('age', 'required|numeric|between:18,120')

    test_cases = [
        ({'age': '25'}, "Age 25"),
        ({'age': '15'}, "Age 15 (too young)"),
        ({'age': '150'}, "Age 150 (too old)"),
        ({'age': 'twenty'}, "Age 'twenty' (not numeric)"),
        ({}, "Missing age"),
    ]

    for data, description in test_cases:
        is_valid = validator.is_valid(data)
        status = "PASS" if is_valid else "FAIL"
        print(f"{description}: {status}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


def custom_error_messages():
    """Using custom error messages"""
    print("=== Custom Error Messages ===")

    validator = Validator()
    validator.add_field('email', 'email', "Please provide a valid email address")
    validator.add_field('age', 'numeric', "Age must be a number")

    data = {
        'email': 'not-an-email',
        'age': 'not-a-number'
    }

    is_valid = validator.is_valid(data)
    print(f"Validation passed: {is_valid}")
    print("Custom error messages:")
    for field, messages in validator.get_errors().items():
        print(f"  {field}: {messages}")
    print()


def optional_fields():
    """Handling optional fields"""
    print("=== Optional Fields ===")

    # Optional fields don't have 'required' rule
    validator = Validator()
    validator.add_field('email', 'email')  # Optional, but must be valid if provided
    validator.add_field('age', 'numeric')  # Optional, but must be numeric if provided

    test_cases = [
        ({'email': 'user@example.com'}, "With email"),
        ({'age': '25'}, "With age"),
        ({}, "No fields"),
        ({'email': 'invalid'}, "Invalid optional email"),
    ]

    for data, description in test_cases:
        is_valid = validator.is_valid(data)
        status = "PASS" if is_valid else "FAIL"
        print(f"{description}: {status}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


def dict_format():
    """Using dictionary format for rules"""
    print("=== Dictionary Format ===")

    # Dict format: {'rule_name': parameters}
    validator = Validator()
    validator.add_field('username', {
        'required': None,
        'alphanum': None,
        'minlen': 3
    })
    validator.add_field('age', {
        'required': None,
        'numeric': None,
        'between': [18, 120]
    })

    test_cases = [
        ({'username': 'alice', 'age': '25'}, "Valid user"),
        ({'username': 'ab', 'age': '25'}, "Username too short"),
        ({'username': 'alice', 'age': '15'}, "Age too low"),
        ({'username': 'alice_123', 'age': '25'}, "Username with underscore"),
    ]

    for data, description in test_cases:
        is_valid = validator.is_valid(data)
        status = "PASS" if is_valid else "FAIL"
        print(f"{description}: {status}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


def user_registration():
    """Practical example: User registration"""
    print("=== User Registration ===")

    validator = Validator()
    validator.add_field('username', 'required|alphanum|minlen:3')
    validator.add_field('email', 'required|email')
    validator.add_field('password', 'required|minlen:8')
    validator.add_field('age', 'numeric|between:13,120')  # Optional

    users = [
        {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'SecurePass123',
            'age': '25'
        },
        {
            'username': 'ab',
            'email': 'bob@example.com',
            'password': 'pass'
        },
        {
            'username': 'charlie',
            'email': 'invalid-email',
            'password': 'Password123'
        },
    ]

    for i, user in enumerate(users, 1):
        is_valid = validator.is_valid(user)
        status = "PASS" if is_valid else "FAIL"
        print(f"User {i} ({user.get('username', 'N/A')}): {status}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


if __name__ == '__main__':
    print("Basic Validator Examples\n")
    simple_validation()
    required_fields()
    multiple_rules()
    custom_error_messages()
    optional_fields()
    dict_format()
    user_registration()
