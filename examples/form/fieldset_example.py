"""
Fieldset examples

This example demonstrates:
- Creating fieldsets to group related fields
- Multiple fieldsets in a single form
- Accessing fieldset fields
- Organizing complex forms
"""

from rick.form import Form


def simple_fieldset_form():
    """Form with a single fieldset"""
    print("=== Simple Fieldset Form ===")

    form = Form()

    # Create a fieldset for personal information
    fs = form.fieldset("personal", "Personal Information")
    fs.field("text", "first_name", "First Name", validators="required")
    fs.field("text", "last_name", "Last Name", validators="required")
    fs.field("text", "age", "Age", validators="numeric")

    # Test data
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": "30"
    }

    if form.is_valid(data):
        print("Form validation: PASSED")
        print(f"  Name: {form.get('first_name')} {form.get('last_name')}")
        print(f"  Age: {form.get('age')}")
    else:
        print("Form validation: FAILED")
        print(f"  Errors: {form.get_errors()}")


def multi_fieldset_form():
    """Form with multiple fieldsets"""
    print("\n=== Multi-Fieldset Form ===")

    form = Form()

    # Personal information fieldset
    personal = form.fieldset("personal_info", "Personal Information")
    personal.field("text", "first_name", "First Name", validators="required")
    personal.field("text", "last_name", "Last Name", validators="required")
    personal.field("text", "age", "Age", validators="numeric|between:18,120")

    # Contact information fieldset
    contact = form.fieldset("contact_info", "Contact Information")
    contact.field("email", "email", "Email", validators="required|email")
    contact.field("text", "phone", "Phone", validators="numeric|minlen:10")

    # Address fieldset
    address = form.fieldset("address_info", "Address")
    address.field("text", "street", "Street", validators="required")
    address.field("text", "city", "City", validators="required")
    address.field("text", "zip_code", "ZIP Code", validators="required")

    # Test complete data
    complete_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "age": "28",
        "email": "alice@example.com",
        "phone": "5551234567",
        "street": "123 Main St",
        "city": "Springfield",
        "zip_code": "12345"
    }

    print("\nTest 1: Complete data")
    if form.is_valid(complete_data):
        print("  Status: VALID")
        print("  Personal:")
        print(f"    Name: {form.get('first_name')} {form.get('last_name')}")
        print(f"    Age: {form.get('age')}")
        print("  Contact:")
        print(f"    Email: {form.get('email')}")
        print(f"    Phone: {form.get('phone')}")
        print("  Address:")
        print(f"    {form.get('street')}, {form.get('city')} {form.get('zip_code')}")

    # Test incomplete data
    incomplete_data = {
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "invalid-email",
        "phone": "555"
    }

    print("\nTest 2: Incomplete data")
    if form.is_valid(incomplete_data):
        print("  Status: VALID")
    else:
        print("  Status: INVALID")
        for field, errors in form.get_errors().items():
            print(f"  {field}: {errors}")


def employee_registration_form():
    """Employee registration with multiple fieldsets"""
    print("\n=== Employee Registration Form ===")

    form = Form()

    # Basic information
    basic = form.fieldset("basic", "Basic Information")
    basic.field("text", "employee_id", "Employee ID", validators="required|alphanum")
    basic.field("text", "first_name", "First Name", validators="required")
    basic.field("text", "last_name", "Last Name", validators="required")
    basic.field("text", "department", "Department", validators="required")

    # Employment details
    employment = form.fieldset("employment", "Employment Details")
    employment.field("date", "start_date", "Start Date", validators="required")
    employment.field("text", "position", "Position", validators="required")
    employment.field("text", "salary", "Salary", validators="numeric")

    # Emergency contact
    emergency = form.fieldset("emergency", "Emergency Contact")
    emergency.field("text", "contact_name", "Contact Name", validators="required")
    emergency.field("text", "contact_phone", "Contact Phone", validators="required|numeric")
    emergency.field("text", "relationship", "Relationship", validators="required")

    employees = [
        {
            "employee_id": "EMP001",
            "first_name": "John",
            "last_name": "Doe",
            "department": "Engineering",
            "start_date": "2024-01-15",
            "position": "Software Engineer",
            "salary": "75000",
            "contact_name": "Jane Doe",
            "contact_phone": "5559876543",
            "relationship": "Spouse"
        },
        {
            "employee_id": "EMP002",
            "first_name": "Alice",
            "last_name": "Smith",
            "department": "Marketing",
            "start_date": "2024-02-01",
            "position": "Marketing Manager",
            # Missing salary and emergency contact
        }
    ]

    for emp in employees:
        print(f"\nEmployee: {emp.get('employee_id')}")
        if form.is_valid(emp):
            print("  Registration: SUCCESS")
            print(f"  Name: {form.get('first_name')} {form.get('last_name')}")
            print(f"  Department: {form.get('department')}")
            print(f"  Position: {form.get('position')}")
        else:
            print("  Registration: FAILED")
            for field, errors in form.get_errors().items():
                print(f"  {field}: {errors}")


def survey_form():
    """Survey with categorized questions"""
    print("\n=== Survey Form ===")

    form = Form()

    # Demographics
    demo = form.fieldset("demographics", "Demographics")
    demo.field("text", "age_range", "Age Range", validators="required")
    demo.field("text", "location", "Location", validators="required")
    demo.field("text", "occupation", "Occupation")

    # Product feedback
    feedback = form.fieldset("feedback", "Product Feedback")
    feedback.field("text", "product_rating", "Overall Rating (1-5)",
                   validators="required|numeric|between:1,5")
    feedback.field("textarea", "comments", "Comments", validators="minlen:10")
    feedback.field("text", "recommend", "Would Recommend (Yes/No)", validators="required")

    # Follow-up
    followup = form.fieldset("followup", "Follow-up")
    followup.field("email", "email", "Email (optional)", validators="email")
    followup.field("checkbox", "contact_me", "Contact me with updates")

    survey_data = {
        "age_range": "25-34",
        "location": "New York",
        "occupation": "Engineer",
        "product_rating": "4",
        "comments": "Great product, would recommend to others!",
        "recommend": "Yes",
        "email": "user@example.com",
        "contact_me": "1"
    }

    print("\nSurvey submission:")
    if form.is_valid(survey_data):
        print("  Status: SUBMITTED")
        print(f"  Rating: {form.get('product_rating')}/5")
        print(f"  Would recommend: {form.get('recommend')}")
        if form.get('email'):
            print(f"  Follow-up email: {form.get('email')}")


def accessing_fieldsets():
    """Demonstrate accessing fieldset information"""
    print("\n=== Accessing Fieldsets ===")

    form = Form()

    form.fieldset("section1", "Section 1").field("text", "field1", "Field 1")
    form.fieldset("section2", "Section 2").field("text", "field2", "Field 2")
    form.fieldset("section3", "Section 3").field("text", "field3", "Field 3")

    # Get all fieldsets
    fieldsets = form.get_fieldsets()

    print("Form structure:")
    for fs_id, fs in fieldsets.items():
        if fs_id != Form.DEFAULT_FIELDSET or fs.label:  # Skip default if empty
            print(f"  Fieldset: {fs_id}")
            print(f"    Label: {fs.label}")
            print(f"    Fields: {list(fs.fields.keys())}")


if __name__ == '__main__':
    print("Fieldset Examples\n")
    simple_fieldset_form()
    multi_fieldset_form()
    employee_registration_form()
    survey_form()
    accessing_fieldsets()
