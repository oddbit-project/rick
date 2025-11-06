"""
String validator rules examples

This example demonstrates:
- Alpha (alphabetic characters)
- AlphaNum (alphanumeric characters)
- Slug (URL-safe slugs)
- Len (exact length)
- MinLen/MaxLen (length constraints)
"""

from rick.validator import Validator


def alpha_validation():
    """Validate alphabetic strings"""
    print("=== Alpha Validation ===")

    validator = Validator()
    validator.add_field('name', 'alpha')

    test_values = [
        'John',
        'MaryJane',
        'John123',  # Invalid: contains numbers
        'Mary-Jane',  # Invalid: contains hyphen
    ]

    for value in test_values:
        is_valid = validator.is_valid({'name': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def alphanum_validation():
    """Validate alphanumeric strings"""
    print("=== AlphaNum Validation ===")

    validator = Validator()
    validator.add_field('username', 'alphanum')

    test_values = [
        'user123',
        'JohnDoe',
        'alice_bob',  # Invalid: contains underscore
        'user-name',  # Invalid: contains hyphen
        '123',
    ]

    for value in test_values:
        is_valid = validator.is_valid({'username': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def slug_validation():
    """Validate URL-safe slugs"""
    print("=== Slug Validation ===")

    validator = Validator()
    validator.add_field('slug', 'slug')

    test_values = [
        'my-blog-post',
        'article_2024',
        'hello-world-123',
        'My Blog Post',  # Invalid: contains spaces and capitals
        'post#1',  # Invalid: contains #
    ]

    for value in test_values:
        is_valid = validator.is_valid({'slug': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def exact_length_validation():
    """Validate exact string length"""
    print("=== Exact Length Validation ===")

    # Validate 5-character codes (using len with same min/max for exact length)
    validator = Validator()
    validator.add_field('code', {'len': [5, 5]})

    test_values = [
        'ABCDE',  # Exactly 5
        'ABC',  # Too short
        'ABCDEFG',  # Too long
        '12345',  # Exactly 5 (numbers)
    ]

    for value in test_values:
        is_valid = validator.is_valid({'code': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}' (len={len(value)}): {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def min_length_validation():
    """Validate minimum string length"""
    print("=== Minimum Length Validation ===")

    validator = Validator()
    validator.add_field('password', 'minlen:8')

    test_values = [
        'pass',  # Too short
        'password',  # Exactly 8
        'MySecurePassword123',  # Longer than 8
        '',  # Empty
    ]

    for value in test_values:
        is_valid = validator.is_valid({'password': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}' (len={len(value)}): {status}")
        if not is_valid:
            print(f"    Error: {validator.get_errors()}")
    print()


def combined_string_rules():
    """Combining multiple string rules"""
    print("=== Combined String Rules ===")

    # Username must be alphanumeric and at least 3 characters
    validator = Validator()
    validator.add_field('username', 'required|alphanum|minlen:3')

    test_values = [
        'alice',  # Valid
        'user123',  # Valid
        'ab',  # Too short
        'user_name',  # Invalid characters
        '',  # Empty
    ]

    for value in test_values:
        is_valid = validator.is_valid({'username': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  '{value}': {status}")
        if not is_valid:
            print(f"    Errors: {validator.get_errors()}")
    print()


def url_slug_generator():
    """Practical example: URL slug validation"""
    print("=== URL Slug Generator ===")

    validator = Validator()
    validator.add_field('slug', 'required|slug|minlen:3')

    articles = [
        {'title': 'My First Blog Post', 'slug': 'my-first-blog-post'},
        {'title': 'Python Tips', 'slug': 'python-tips'},
        {'title': 'Invalid Slug', 'slug': 'Invalid Slug!'},  # Invalid
        {'title': 'Too Short', 'slug': 'ab'},  # Too short
    ]

    for article in articles:
        is_valid = validator.is_valid({'slug': article['slug']})
        status = "PASS" if is_valid else "FAIL"
        print(f"Title: {article['title']}")
        print(f"  Slug: '{article['slug']}' - {status}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


if __name__ == '__main__':
    print("String Validation Examples\n")
    alpha_validation()
    alphanum_validation()
    slug_validation()
    exact_length_validation()
    min_length_validation()
    combined_string_rules()
    url_slug_generator()
