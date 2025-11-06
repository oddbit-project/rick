"""
RequestRecord examples

This example demonstrates:
- Using RequestRecord for API request validation
- Field specifications with field() helper
- Binding form data to objects
- Nested records and recordsets
"""

from rick.form import RequestRecord, field, record, recordset


class UserRecord(RequestRecord):
    """Simple user record"""
    fields = {
        'username': field(validators='required|alphanum|minlen:3'),
        'email': field(validators='required|email'),
        'age': field(validators='numeric|between:13,120'),
    }


class AddressRecord(RequestRecord):
    """Address record"""
    fields = {
        'street': field(validators='required'),
        'city': field(validators='required'),
        'state': field(validators='required|len:2,2'),
        'zip_code': field(validators='required|numeric|len:5,5'),
    }


class ContactRecord(RequestRecord):
    """Contact with nested address"""
    fields = {
        'name': field(validators='required'),
        'email': field(validators='required|email'),
        'phone': field(validators='numeric'),
        'address': record(AddressRecord, required=True),
    }


class OrderItemRecord(RequestRecord):
    """Individual order item"""
    fields = {
        'product_id': field(validators='required'),
        'quantity': field(validators='required|numeric|between:1,100'),
        'price': field(validators='required|decimal'),
    }


class OrderRecord(RequestRecord):
    """Order with multiple items"""
    fields = {
        'order_id': field(validators='required'),
        'customer_email': field(validators='required|email'),
        'items': recordset(OrderItemRecord, required=True),
    }


def simple_request_record():
    """Basic RequestRecord usage"""
    print("=== Simple RequestRecord ===")

    record = UserRecord()

    users = [
        {'username': 'alice123', 'email': 'alice@example.com', 'age': '25'},
        {'username': 'ab', 'email': 'bob@test.com', 'age': '30'},
        {'username': 'charlie', 'email': 'invalid-email', 'age': '20'},
    ]

    for user in users:
        print(f"\nUser: {user['username']}")
        if record.is_valid(user):
            print("  Status: VALID")
            print(f"  Data: {record.get_data()}")
        else:
            print("  Status: INVALID")
            print(f"  Errors: {record.get_errors()}")


def nested_record_example():
    """Nested record validation"""
    print("\n=== Nested Record Example ===")

    record = ContactRecord()

    contacts = [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '5551234567',
            'address': {
                'street': '123 Main St',
                'city': 'Springfield',
                'state': 'IL',
                'zip_code': '62701'
            }
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'phone': '5559876543',
            'address': {
                'street': '456 Oak Ave',
                'city': 'Chicago',
                'state': 'Illinois',  # Invalid: too long
                'zip_code': '60601'
            }
        },
        {
            'name': 'Bob Jones',
            'email': 'bob@test.com',
            # Missing required address
        }
    ]

    for contact in contacts:
        print(f"\nContact: {contact['name']}")
        if record.is_valid(contact):
            print("  Status: VALID")
            data = record.get_data()
            print(f"  Email: {data['email']}")
            print(f"  Address: {data['address']['city']}, {data['address']['state']}")
        else:
            print("  Status: INVALID")
            print(f"  Errors: {record.get_errors()}")


def recordset_example():
    """Recordset (list of records) validation"""
    print("\n=== Recordset Example ===")

    record = OrderRecord()

    orders = [
        {
            'order_id': 'ORD001',
            'customer_email': 'customer@example.com',
            'items': [
                {'product_id': 'PROD1', 'quantity': '2', 'price': '19.99'},
                {'product_id': 'PROD2', 'quantity': '1', 'price': '29.99'},
            ]
        },
        {
            'order_id': 'ORD002',
            'customer_email': 'invalid-email',
            'items': [
                {'product_id': 'PROD3', 'quantity': '0', 'price': '15.00'},  # Invalid qty
                {'product_id': '', 'quantity': '5', 'price': '25.00'},  # Missing product_id
            ]
        },
    ]

    for order in orders:
        print(f"\nOrder: {order['order_id']}")
        if record.is_valid(order):
            print("  Status: VALID")
            data = record.get_data()
            print(f"  Customer: {data['customer_email']}")
            print(f"  Items: {len(data['items'])}")
            total = sum(float(item['price']) * int(item['quantity'])
                        for item in data['items'])
            print(f"  Total: ${total:.2f}")
        else:
            print("  Status: INVALID")
            errors = record.get_errors()
            print(f"  Errors: {errors}")


def binding_to_objects():
    """Binding form data to Python objects"""
    print("\n=== Binding to Objects ===")

    class User:
        def __init__(self):
            self.username = None
            self.email = None
            self.age = None

        def __repr__(self):
            return f"User(username={self.username}, email={self.email}, age={self.age})"

    record = UserRecord()
    data = {
        'username': 'alice123',
        'email': 'alice@example.com',
        'age': '25'
    }

    if record.is_valid(data):
        print("Valid data, binding to object...")

        # Bind to a new instance
        user = record.bind(User)
        print(f"  Bound object: {user}")

        # Can also bind to an existing instance
        existing_user = User()
        existing_user.username = "old_value"
        user2 = record.bind(existing_user)
        print(f"  Updated object: {user2}")


def custom_field_binding():
    """Custom field name binding"""
    print("\n=== Custom Field Binding ===")

    class DatabaseRecord(RequestRecord):
        """Record with custom bind names"""
        fields = {
            'user_name': field(validators='required', bind='username'),
            'user_email': field(validators='required|email', bind='email'),
            'user_age': field(validators='numeric', bind='age'),
        }

    class DbUser:
        def __init__(self):
            self.username = None
            self.email = None
            self.age = None

        def __repr__(self):
            return f"DbUser(username={self.username}, email={self.email}, age={self.age})"

    record = DatabaseRecord()
    form_data = {
        'user_name': 'john_doe',
        'user_email': 'john@example.com',
        'user_age': '30'
    }

    if record.is_valid(form_data):
        print("Form data validated")
        print(f"  Form fields: {list(record.get_data().keys())}")

        # Bind using custom bind names
        db_user = record.bind(DbUser)
        print(f"  Database object: {db_user}")


def bindx_example():
    """Using bindx to get unmapped values"""
    print("\n=== BindX Example ===")

    class UserModel:
        def __init__(self):
            self.username = None
            self.email = None

    record = UserRecord()
    data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'age': '25'  # This won't map to UserModel
    }

    if record.is_valid(data):
        user, unmapped = record.bindx(UserModel)
        print("Bound to object:")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Unmapped values: {unmapped}")


def api_request_validation():
    """Simulating API request validation"""
    print("\n=== API Request Validation ===")

    class CreateUserRequest(RequestRecord):
        """API request to create a user"""
        fields = {
            'username': field(validators='required|alphanum|minlen:3|maxlen:20'),
            'email': field(validators='required|email'),
            'password': field(validators='required|minlen:8'),
            'full_name': field(validators='required'),
            'role': field(validators='required'),
        }

    # Simulate API requests
    requests = [
        {
            'username': 'alice123',
            'email': 'alice@example.com',
            'password': 'SecurePass123',
            'full_name': 'Alice Smith',
            'role': 'user'
        },
        {
            'username': 'ab',  # Too short
            'email': 'bob@test.com',
            'password': 'short',  # Too short
            'full_name': 'Bob Jones',
            'role': 'admin'
        }
    ]

    validator = CreateUserRequest()

    for i, req in enumerate(requests, 1):
        print(f"\nAPI Request {i}:")
        if validator.is_valid(req):
            print("  Response: 200 OK")
            print(f"  Created user: {req['username']}")
        else:
            print("  Response: 400 Bad Request")
            print(f"  Errors: {validator.get_errors()}")


if __name__ == '__main__':
    print("RequestRecord Examples\n")
    simple_request_record()
    nested_record_example()
    recordset_example()
    binding_to_objects()
    custom_field_binding()
    bindx_example()
    api_request_validation()
