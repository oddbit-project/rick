"""
Numeric validator rules examples

This example demonstrates:
- Numeric (validate numbers)
- Int (validate integers)
- Decimal (validate decimal numbers)
- Between (validate range)
"""

from rick.validator import Validator


def numeric_validation():
    """Validate numeric values"""
    print("=== Numeric Validation ===")

    validator = Validator()
    validator.add_field('value', 'numeric')

    test_values = [
        '123',
        '45.67',
        '-10',
        '0',
        'not-a-number',
        '12.34.56',  # Invalid format
    ]

    for value in test_values:
        is_valid = validator.is_valid({'value': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
    print()


def integer_validation():
    """Validate integer values"""
    print("=== Integer Validation ===")

    validator = Validator()
    validator.add_field('count', 'int')

    test_values = [
        '10',
        '0',
        '-5',
        '3.14',  # Invalid: decimal
        'ten',  # Invalid: not numeric
        '100',
    ]

    for value in test_values:
        is_valid = validator.is_valid({'count': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
    print()


def decimal_validation():
    """Validate decimal values"""
    print("=== Decimal Validation ===")

    validator = Validator()
    validator.add_field('price', 'decimal')

    test_values = [
        '19.99',
        '100',
        '0.50',
        '-25.00',
        'not-a-number',
    ]

    for value in test_values:
        is_valid = validator.is_valid({'price': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
    print()


def between_validation():
    """Validate values within a range"""
    print("=== Between Validation ===")

    # Age between 18 and 120
    validator = Validator()
    validator.add_field('age', 'between:18,120')

    test_values = [
        '25',  # Valid
        '18',  # Valid (minimum)
        '120',  # Valid (maximum)
        '17',  # Too young
        '121',  # Too old
        '50',  # Valid
    ]

    for value in test_values:
        is_valid = validator.is_valid({'age': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  Age {value}: {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def combined_numeric_rules():
    """Combining multiple numeric rules"""
    print("=== Combined Numeric Rules ===")

    # Quantity: required integer between 1 and 100
    validator = Validator()
    validator.add_field('quantity', 'required|int|between:1,100')

    test_values = [
        '10',  # Valid
        '1',  # Valid (minimum)
        '100',  # Valid (maximum)
        '0',  # Too low
        '101',  # Too high
        '10.5',  # Not an integer
        '',  # Required
    ]

    for value in test_values:
        is_valid = validator.is_valid({'quantity': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
        if not is_valid:
            print(f"    Errors: {validator.get_errors()}")
    print()


def price_validation():
    """Practical example: Product price validation"""
    print("=== Product Price Validation ===")

    validator = Validator()
    validator.add_field('price', 'required|decimal|between:0.01,9999.99')

    products = [
        {'name': 'Widget', 'price': '19.99'},
        {'name': 'Gadget', 'price': '0.50'},
        {'name': 'Free Item', 'price': '0.00'},  # Too low
        {'name': 'Expensive', 'price': '10000.00'},  # Too high
        {'name': 'Invalid', 'price': 'free'},  # Not a number
    ]

    for product in products:
        is_valid = validator.is_valid({'price': product['price']})
        status = "PASS" if is_valid else "FAIL"
        print(f"Product: {product['name']}")
        print(f"  Price: ${product['price']} - {status}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


def rating_system():
    """Rating system validation (1-5 stars)"""
    print("=== Rating System ===")

    validator = Validator()
    validator.add_field('rating', 'required|int|between:1,5')

    ratings = ['1', '3', '5', '0', '6', 'three']

    for rating in ratings:
        is_valid = validator.is_valid({'rating': rating})
        status = "PASS" if is_valid else "FAIL"
        stars = '*' * int(rating) if status == "PASS" else ''
        print(f"  Rating {rating}: {status} {stars}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def percentage_validation():
    """Validate percentage values"""
    print("=== Percentage Validation ===")

    validator = Validator()
    validator.add_field('percentage', 'required|numeric|between:0,100')

    test_values = ['0', '50', '100', '101', '-5', '75.5']

    for value in test_values:
        is_valid = validator.is_valid({'percentage': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}%: {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


if __name__ == '__main__':
    print("Numeric Validation Examples\n")
    numeric_validation()
    integer_validation()
    decimal_validation()
    between_validation()
    combined_numeric_rules()
    price_validation()
    rating_system()
    percentage_validation()
