"""
Custom validation examples

This example demonstrates:
- Custom validator methods
- Adding manual errors
- Validating related fields
- Business logic validation
"""

from rick.form import Form
from rick.mixin import Translator


class PasswordConfirmForm(Form):
    """Form with custom password confirmation validation"""

    def __init__(self, translator: Translator = None):
        super().__init__(translator)
        self.field("text", "username", "Username", validators="required|minlen:3")
        self.field("password", "password", "Password", validators="required|minlen:8")
        self.field("password", "password_confirm", "Confirm Password", validators="required")

    def validator_password_confirm(self, data, t: Translator):
        """Custom validator to check password confirmation matches"""
        if data.get('password') != data.get('password_confirm'):
            self.add_error('password_confirm', 'Passwords do not match')
            return False
        return True


class AgeVerificationForm(Form):
    """Form with custom age verification"""

    def __init__(self, translator: Translator = None):
        super().__init__(translator)
        self.field("text", "name", "Name", validators="required")
        self.field("text", "age", "Age", validators="required|numeric")
        self.field("checkbox", "agree_terms", "I agree to terms")

    def validator_age(self, data, t: Translator):
        """Custom validator to check minimum age"""
        age = int(data.get('age', 0))
        if age < 18:
            self.add_error('age', 'You must be at least 18 years old')
            return False
        return True

    def validator_agree_terms(self, data, t: Translator):
        """Custom validator to check terms agreement"""
        if not data.get('agree_terms'):
            self.add_error('agree_terms', 'You must agree to the terms')
            return False
        return True


class ProhibitedNamesForm(Form):
    """Form that rejects certain usernames"""

    PROHIBITED_NAMES = ['admin', 'root', 'system', 'test']

    def __init__(self, translator: Translator = None):
        super().__init__(translator)
        self.field("text", "username", "Username", validators="required|alphanum")
        self.field("email", "email", "Email", validators="required|email")

    def validator_username(self, data, t: Translator):
        """Custom validator to check prohibited usernames"""
        username = data.get('username', '').lower()
        if username in self.PROHIBITED_NAMES:
            self.add_error('username', f'Username "{username}" is not allowed')
            return False
        return True


class DateRangeForm(Form):
    """Form with date range validation"""

    def __init__(self, translator: Translator = None):
        super().__init__(translator)
        self.field("date", "start_date", "Start Date", validators="required")
        self.field("date", "end_date", "End Date", validators="required")

    def validator_end_date(self, data, t: Translator):
        """Custom validator to ensure end_date is after start_date"""
        start = data.get('start_date', '')
        end = data.get('end_date', '')

        if start and end and end < start:
            self.add_error('end_date', 'End date must be after start date')
            return False
        return True


def test_password_confirmation():
    """Test password confirmation validation"""
    print("=== Password Confirmation Validation ===")

    form = PasswordConfirmForm()

    test_cases = [
        {
            "username": "alice",
            "password": "SecurePass123",
            "password_confirm": "SecurePass123"
        },
        {
            "username": "bob",
            "password": "Password123",
            "password_confirm": "DifferentPass"
        },
        {
            "username": "charlie",
            "password": "short",
            "password_confirm": "short"
        }
    ]

    for data in test_cases:
        print(f"\nUsername: {data['username']}")
        if form.is_valid(data):
            print("  Status: VALID")
            print("  Password confirmed successfully")
        else:
            print("  Status: INVALID")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


def test_age_verification():
    """Test age verification"""
    print("\n=== Age Verification ===")

    form = AgeVerificationForm()

    users = [
        {"name": "John", "age": "25", "agree_terms": "1"},
        {"name": "Jane", "age": "16", "agree_terms": "1"},
        {"name": "Bob", "age": "30", "agree_terms": ""},
    ]

    for user in users:
        print(f"\nUser: {user['name']}, Age: {user['age']}")
        if form.is_valid(user):
            print("  Status: VERIFIED")
        else:
            print("  Status: REJECTED")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


def test_prohibited_names():
    """Test prohibited usernames"""
    print("\n=== Prohibited Usernames ===")

    form = ProhibitedNamesForm()

    users = [
        {"username": "alice123", "email": "alice@example.com"},
        {"username": "admin", "email": "admin@example.com"},
        {"username": "root", "email": "root@system.com"},
        {"username": "john", "email": "john@test.com"},
    ]

    for user in users:
        print(f"\nUsername: {user['username']}")
        if form.is_valid(user):
            print("  Status: ACCEPTED")
        else:
            print("  Status: REJECTED")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


def test_date_range():
    """Test date range validation"""
    print("\n=== Date Range Validation ===")

    form = DateRangeForm()

    date_ranges = [
        {"start_date": "2024-01-01", "end_date": "2024-01-31"},
        {"start_date": "2024-06-01", "end_date": "2024-05-01"},  # Invalid
        {"start_date": "2024-03-15", "end_date": "2024-03-15"},  # Same day
    ]

    for i, dates in enumerate(date_ranges, 1):
        print(f"\nRange {i}: {dates['start_date']} to {dates['end_date']}")
        if form.is_valid(dates):
            print("  Status: VALID")
        else:
            print("  Status: INVALID")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


def manual_error_example():
    """Demonstrate adding errors manually"""
    print("\n=== Manual Error Handling ===")

    form = Form()
    form.field("text", "username", "Username", validators="required")
    form.field("email", "email", "Email", validators="required|email")

    data = {"username": "testuser", "email": "test@example.com"}

    if form.is_valid(data):
        # Simulate checking if username already exists
        username_exists = True  # Pretend we checked a database

        if username_exists:
            form.add_error('username', 'Username already taken')
            print("Validation failed:")
            print(f"  Errors: {form.get_errors()}")
        else:
            print("User can be registered")


def complex_business_logic():
    """Complex business logic validation"""
    print("\n=== Complex Business Logic ===")

    class OrderForm(Form):
        def __init__(self, translator: Translator = None):
            super().__init__(translator)
            self.field("text", "product_id", "Product ID", validators="required")
            self.field("text", "quantity", "Quantity", validators="required|numeric|between:1,100")
            self.field("text", "coupon_code", "Coupon Code")

        def validator_quantity(self, data, t: Translator):
            """Check if quantity is available in stock"""
            quantity = int(data.get('quantity', 0))
            stock = 50  # Pretend we checked stock

            if quantity > stock:
                self.add_error('quantity', f'Only {stock} items available in stock')
                return False
            return True

        def validator_coupon_code(self, data, t: Translator):
            """Validate coupon code"""
            coupon = data.get('coupon_code', '').upper()
            valid_coupons = ['SAVE10', 'WELCOME', 'SPECIAL']

            if coupon and coupon not in valid_coupons:
                self.add_error('coupon_code', 'Invalid coupon code')
                return False
            return True

    form = OrderForm()

    orders = [
        {"product_id": "PROD123", "quantity": "10", "coupon_code": "SAVE10"},
        {"product_id": "PROD456", "quantity": "75", "coupon_code": ""},
        {"product_id": "PROD789", "quantity": "5", "coupon_code": "INVALID"},
    ]

    for order in orders:
        print(f"\nOrder for Product {order['product_id']}, Qty: {order['quantity']}")
        if form.is_valid(order):
            print("  Status: ACCEPTED")
            print(f"  Total items: {form.get('quantity')}")
            if form.get('coupon_code'):
                print(f"  Coupon applied: {form.get('coupon_code')}")
        else:
            print("  Status: REJECTED")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


if __name__ == '__main__':
    print("Custom Validation Examples\n")
    test_password_confirmation()
    test_age_verification()
    test_prohibited_names()
    test_date_range()
    manual_error_example()
    complex_business_logic()
