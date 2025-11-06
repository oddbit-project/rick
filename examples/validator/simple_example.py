"""
Simple validator example

Demonstrates basic validator usage with the Rick validator
"""

from rick.validator import Validator


def main():
    """Basic validator usage"""

    # Create validator with rules
    validator = Validator()
    validator.add_field('email', 'required|email')
    validator.add_field('age', 'required|numeric|between:18,120')
    validator.add_field('username', 'required|alphanum|minlen:3')

    # Test valid data
    print("=== Valid Data ===")
    valid_data = {
        'email': 'user@example.com',
        'age': '25',
        'username': 'alice'
    }

    if validator.is_valid(valid_data):
        print("PASS: Data is valid")
        print(f"Data: {valid_data}")
    else:
        print("FAIL: Data is invalid")
        print(f"Errors: {validator.get_errors()}")
    print()

    # Test invalid data
    print("=== Invalid Data ===")
    invalid_data = {
        'email': 'not-an-email',
        'age': '15',  # Too young
        'username': 'ab'  # Too short
    }

    if validator.is_valid(invalid_data):
        print("PASS: Data is valid")
    else:
        print("FAIL: Data is invalid")
        print(f"Errors: {validator.get_errors()}")
    print()

    # Test missing required fields
    print("=== Missing Required Fields ===")
    incomplete_data = {
        'email': 'user@example.com'
        # age and username missing
    }

    if validator.is_valid(incomplete_data):
        print("PASS: Data is valid")
    else:
        print("FAIL: Data is invalid")
        print(f"Errors: {validator.get_errors()}")


if __name__ == '__main__':
    main()
