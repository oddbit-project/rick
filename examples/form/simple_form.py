"""
Simple form example

This example demonstrates:
- Creating a basic form
- Adding fields with validation
- Validating form data
- Accessing field values
- Handling validation errors
"""

from rick.form import Form


def simple_contact_form():
    """Basic contact form example"""
    print("=== Simple Contact Form ===")

    # Create form
    form = Form()

    # Add fields with validation
    form.field("text", "name", "Full Name", validators="required|minlen:3|maxlen:50")
    form.field("email", "email", "Email", validators="required|email")
    form.field("text", "subject", "Subject", validators="required|minlen:5")
    form.field("textarea", "message", "Message", validators="required|minlen:10")

    # Test data
    test_data = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Question about product",
            "message": "I would like to know more about your products."
        },
        {
            "name": "Jo",  # Too short
            "email": "invalid-email",
            "subject": "Hi",  # Too short
            "message": "Short"  # Too short
        },
        {
            "name": "Alice Smith",
            "email": "alice@company.com",
            "subject": "",  # Missing required field
            "message": "Looking forward to hearing from you!"
        }
    ]

    for i, data in enumerate(test_data, 1):
        print(f"\nTest {i}:")
        is_valid = form.is_valid(data)

        if is_valid:
            print("  Status: VALID")
            print(f"  Name: {form.get('name')}")
            print(f"  Email: {form.get('email')}")
            print(f"  Subject: {form.get('subject')}")
        else:
            print("  Status: INVALID")
            print(f"  Errors: {form.get_errors()}")


def user_registration_form():
    """User registration form with password validation"""
    print("\n=== User Registration Form ===")

    form = Form()

    # Add registration fields
    form.field("text", "username", "Username",
               validators="required|alphanum|minlen:3|maxlen:20")
    form.field("email", "email", "Email", validators="required|email")
    form.field("password", "password", "Password", validators="required|minlen:8")
    form.field("text", "age", "Age", validators="numeric|between:13,120")

    # Test cases
    users = [
        {
            "username": "alice123",
            "email": "alice@example.com",
            "password": "SecurePass123",
            "age": "25"
        },
        {
            "username": "ab",  # Too short
            "email": "bob@test.com",
            "password": "short",  # Too short
            "age": "30"
        },
        {
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "LongPassword123",
            "age": "150"  # Out of range
        }
    ]

    for user in users:
        print(f"\nUser: {user['username']}")
        if form.is_valid(user):
            print("  Registration: SUCCESS")
            print(f"  Username: {form.get('username')}")
            print(f"  Email: {form.get('email')}")
            if form.get('age'):
                print(f"  Age: {form.get('age')}")
        else:
            print("  Registration: FAILED")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


def login_form():
    """Simple login form"""
    print("\n=== Login Form ===")

    form = Form()
    form.field("text", "username", "Username", validators="required")
    form.field("password", "password", "Password", validators="required")

    # Test logins
    logins = [
        {"username": "admin", "password": "secret123"},
        {"password": "password"},  # Missing username
        {"username": "user"},  # Missing password
    ]

    for login in logins:
        is_valid = form.is_valid(login)
        status = "VALID" if is_valid else "INVALID"
        print(f"\nLogin attempt: {status}")
        if 'username' in login:
            print(f"  Username: {login.get('username')}")
        if 'password' in login:
            print(f"  Password: {'*' * len(login.get('password', ''))}")

        if not is_valid:
            print(f"  Errors: {form.get_errors()}")


def form_with_get_data():
    """Demonstrate getting all form data at once"""
    print("\n=== Form Data Retrieval ===")

    form = Form()
    form.field("text", "first_name", "First Name", validators="required")
    form.field("text", "last_name", "Last Name", validators="required")
    form.field("email", "email", "Email", validators="required|email")
    form.field("text", "phone", "Phone", validators="numeric")

    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "5551234567"
    }

    if form.is_valid(data):
        print("Form is valid!")
        print("\nAll form data:")
        for field, value in form.get_data().items():
            print(f"  {field}: {value}")


def form_with_set_values():
    """Demonstrate setting field values programmatically"""
    print("\n=== Setting Field Values ===")

    form = Form()
    form.field("text", "name", "Name", validators="required")
    form.field("email", "email", "Email", validators="required|email")
    form.field("text", "country", "Country")

    # Set values programmatically
    form.set("name", "Alice")
    form.set("email", "alice@example.com")
    form.set("country", "USA")

    print("Field values set programmatically:")
    print(f"  Name: {form.get('name')}")
    print(f"  Email: {form.get('email')}")
    print(f"  Country: {form.get('country')}")


if __name__ == '__main__':
    print("Rick Form Examples\n")
    simple_contact_form()
    user_registration_form()
    login_form()
    form_with_get_data()
    form_with_set_values()
