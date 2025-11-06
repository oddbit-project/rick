"""
Network validator rules examples

This example demonstrates:
- IPv4 (validate IPv4 addresses)
- IPv6 (validate IPv6 addresses)
- IP (validate either IPv4 or IPv6)
- Email (validate email addresses)
- Fqdn (validate fully qualified domain names)
- Mac (validate MAC addresses)
"""

from rick.validator import Validator


def ipv4_validation():
    """Validate IPv4 addresses"""
    print("=== IPv4 Validation ===")

    validator = Validator()
    validator.add_field('ip', 'ipv4')

    test_values = [
        '192.168.1.1',
        '10.0.0.1',
        '127.0.0.1',
        '255.255.255.255',
        '256.1.1.1',  # Invalid: out of range
        '192.168.1',  # Invalid: incomplete
        'not-an-ip',  # Invalid
    ]

    for value in test_values:
        is_valid = validator.is_valid({'ip': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}: {status}")
    print()


def ipv6_validation():
    """Validate IPv6 addresses"""
    print("=== IPv6 Validation ===")

    validator = Validator()
    validator.add_field('ip', 'ipv6')

    test_values = [
        '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        '2001:db8:85a3::8a2e:370:7334',  # Compressed
        '::1',  # Loopback
        '::',  # All zeros
        'fe80::1',
        '192.168.1.1',  # Invalid: IPv4
        'not-an-ip',  # Invalid
    ]

    for value in test_values:
        is_valid = validator.is_valid({'ip': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}: {status}")
    print()


def ip_any_version():
    """Validate IPv4 or IPv6"""
    print("=== IP (Any Version) ===")

    validator = Validator()
    validator.add_field('ip', 'ip')

    test_values = [
        '192.168.1.1',  # IPv4
        '10.0.0.1',  # IPv4
        '2001:db8::1',  # IPv6
        '::1',  # IPv6
        'not-an-ip',  # Invalid
    ]

    for value in test_values:
        is_valid = validator.is_valid({'ip': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}: {status}")
    print()


def email_validation():
    """Validate email addresses"""
    print("=== Email Validation ===")

    validator = Validator()
    validator.add_field('email', 'email')

    test_values = [
        'user@example.com',
        'alice.smith@company.co.uk',
        'test+tag@domain.com',
        'name@subdomain.example.com',
        'invalid-email',  # Missing @
        '@example.com',  # Missing local part
        'user@',  # Missing domain
    ]

    for value in test_values:
        is_valid = validator.is_valid({'email': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}: {status}")
    print()


def fqdn_validation():
    """Validate fully qualified domain names"""
    print("=== FQDN Validation ===")

    validator = Validator()
    validator.add_field('domain', 'fqdn')

    test_values = [
        'example.com',
        'subdomain.example.com',
        'www.example.co.uk',
        'api.v2.example.com',
        'example',  # Invalid: missing TLD
        '-example.com',  # Invalid: starts with hyphen
    ]

    for value in test_values:
        is_valid = validator.is_valid({'domain': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}: {status}")
    print()


def mac_validation():
    """Validate MAC addresses"""
    print("=== MAC Address Validation ===")

    validator = Validator()
    validator.add_field('mac', 'mac')

    test_values = [
        '00:1A:2B:3C:4D:5E',
        '00-1A-2B-3C-4D-5E',
        '001A.2B3C.4D5E',  # Cisco format
        'FF:FF:FF:FF:FF:FF',
        '00:00:00:00:00:00',
        '00:1A:2B:3C:4D',  # Invalid: incomplete
        'not-a-mac',  # Invalid
    ]

    for value in test_values:
        is_valid = validator.is_valid({'mac': value})
        status = "PASS" if is_valid else "FAIL"
        print(f"  {value}: {status}")
    print()


def user_registration():
    """Practical example: User registration"""
    print("=== User Registration Form ===")

    validator = Validator()
    validator.add_field('email', 'required|email')
    validator.add_field('website', 'fqdn')  # Optional

    users = [
        {'email': 'alice@example.com', 'website': 'example.com'},
        {'email': 'bob@company.co.uk', 'website': ''},
        {'email': 'invalid-email', 'website': 'example.com'},
        {'email': 'charlie@test.com', 'website': 'invalid domain'},
    ]

    for i, user in enumerate(users, 1):
        is_valid = validator.is_valid(user)
        status = "PASS" if is_valid else "FAIL"
        print(f"User {i}: {status}")
        print(f"  Email: {user['email']}")
        print(f"  Website: {user.get('website') or '(none)'}")
        if not is_valid:
            print(f"  Errors: {validator.get_errors()}")
    print()


def server_config():
    """Server configuration validation"""
    print("=== Server Configuration ===")

    validator = Validator()
    validator.add_field('hostname', 'required|fqdn')
    validator.add_field('ip_address', 'required|ip')
    validator.add_field('admin_email', 'required|email')

    configs = [
        {
            'hostname': 'server1.example.com',
            'ip_address': '192.168.1.100',
            'admin_email': 'admin@example.com'
        },
        {
            'hostname': 'invalid hostname',
            'ip_address': '256.1.1.1',
            'admin_email': 'admin@example.com'
        },
        {
            'hostname': 'server2.example.com',
            'ip_address': '2001:db8::1',
            'admin_email': 'invalid-email'
        },
    ]

    for i, config in enumerate(configs, 1):
        is_valid = validator.is_valid(config)
        status = "PASS" if is_valid else "FAIL"
        print(f"Config {i}: {status}")
        if is_valid:
            print(f"  Hostname: {config['hostname']}")
            print(f"  IP: {config['ip_address']}")
            print(f"  Admin: {config['admin_email']}")
        else:
            print(f"  Errors: {validator.get_errors()}")
    print()


def network_device():
    """Network device information"""
    print("=== Network Device Info ===")

    validator = Validator()
    validator.add_field('device_name', 'required')
    validator.add_field('mac_address', 'required|mac')
    validator.add_field('ip_address', 'required|ipv4')

    devices = [
        {
            'device_name': 'Router-1',
            'mac_address': '00:1A:2B:3C:4D:5E',
            'ip_address': '192.168.1.1'
        },
        {
            'device_name': 'Switch-1',
            'mac_address': 'invalid-mac',
            'ip_address': '192.168.1.2'
        },
    ]

    for device in devices:
        is_valid = validator.is_valid(device)
        status = "PASS" if is_valid else "FAIL"
        print(f"Device: {device['device_name']} - {status}")
        if is_valid:
            print(f"  MAC: {device['mac_address']}")
            print(f"  IP: {device['ip_address']}")
        else:
            print(f"  Errors: {validator.get_errors()}")
    print()


if __name__ == '__main__':
    print("Network Validation Examples\n")
    ipv4_validation()
    ipv6_validation()
    ip_any_version()
    email_validation()
    fqdn_validation()
    mac_validation()
    user_registration()
    server_config()
    network_device()
