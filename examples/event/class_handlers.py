"""
Class-based event handlers

This example demonstrates:
- Creating EventHandler classes
- Accessing DI container in handlers
- Multiple event methods in one class
- Using services from DI container
"""

from rick.base import Di
from rick.event import EventManager, EventHandler


# Mock services for demonstration
class DatabaseService:
    def log_event(self, event_type, user_id):
        print(f"  [DB] Logged event: {event_type} for user {user_id}")

    def update_user(self, user_id, data):
        print(f"  [DB] Updated user {user_id}: {data}")


class CacheService:
    def set(self, key, value):
        print(f"  [CACHE] Set {key} = {value}")

    def delete(self, key):
        print(f"  [CACHE] Deleted {key}")


class EmailService:
    def send(self, to, subject, body):
        print(f"  [EMAIL] Sent to {to}: {subject}")


# Event handler class
class UserEventsHandler(EventHandler):
    """Handles user-related events"""

    def user_created(self, user_id, username, email):
        """Handle user creation"""
        print(f"UserEventsHandler.user_created:")
        print(f"  Creating user: {username} ({email})")

        # Access services from DI container
        db = self.get_di().get('database')
        db.log_event('user_created', user_id)

        cache = self.get_di().get('cache')
        cache.set(f"user:{user_id}", {'username': username, 'email': email})

    def user_updated(self, user_id, username, **kwargs):
        """Handle user updates"""
        print(f"UserEventsHandler.user_updated:")
        print(f"  Updating user: {username}")

        db = self.get_di().get('database')
        db.update_user(user_id, kwargs)

        cache = self.get_di().get('cache')
        cache.delete(f"user:{user_id}")

    def user_deleted(self, user_id, username):
        """Handle user deletion"""
        print(f"UserEventsHandler.user_deleted:")
        print(f"  Deleting user: {username}")

        cache = self.get_di().get('cache')
        cache.delete(f"user:{user_id}")


class NotificationHandler(EventHandler):
    """Handles notification sending"""

    def user_created(self, user_id, username, email):
        """Send welcome email"""
        print(f"NotificationHandler.user_created:")

        mailer = self.get_di().get('mailer')
        mailer.send(
            to=email,
            subject='Welcome!',
            body=f'Welcome {username}!'
        )


class AnalyticsHandler(EventHandler):
    """Handles analytics tracking"""

    def user_created(self, user_id, username, email):
        """Track user creation"""
        print(f"AnalyticsHandler.user_created:")
        print(f"  Tracking new user: {username}")

    def user_deleted(self, user_id, username):
        """Track user deletion"""
        print(f"AnalyticsHandler.user_deleted:")
        print(f"  Tracking deleted user: {username}")


def setup_di():
    """Setup dependency injection container with services"""
    di = Di()
    di.add('database', DatabaseService())
    di.add('cache', CacheService())
    di.add('mailer', EmailService())
    return di


def single_handler():
    """Single class handler"""
    print("=== Single Class Handler ===")

    di = setup_di()
    manager = EventManager()

    # Register handler class
    manager.add_handler(
        'user_created',
        f'{__name__}.UserEventsHandler'
    )

    # Dispatch event
    manager.dispatch(
        di,
        'user_created',
        user_id=123,
        username='alice',
        email='alice@example.com'
    )


def multiple_class_handlers():
    """Multiple class handlers for same event"""
    print("\n=== Multiple Class Handlers ===")

    di = setup_di()
    manager = EventManager()

    # Register multiple handlers
    manager.add_handler(
        'user_created',
        f'{__name__}.UserEventsHandler'
    )
    manager.add_handler(
        'user_created',
        f'{__name__}.NotificationHandler'
    )
    manager.add_handler(
        'user_created',
        f'{__name__}.AnalyticsHandler'
    )

    # Dispatch - all handlers execute
    manager.dispatch(
        di,
        'user_created',
        user_id=456,
        username='bob',
        email='bob@example.com'
    )


def multiple_events_one_class():
    """One class handling multiple events"""
    print("\n=== Multiple Events, One Class ===")

    di = setup_di()
    manager = EventManager()

    # Register same class for different events
    manager.add_handler(
        'user_created',
        f'{__name__}.UserEventsHandler'
    )
    manager.add_handler(
        'user_updated',
        f'{__name__}.UserEventsHandler'
    )
    manager.add_handler(
        'user_deleted',
        f'{__name__}.UserEventsHandler'
    )

    # Dispatch different events
    print("Create user:")
    manager.dispatch(
        di,
        'user_created',
        user_id=789,
        username='charlie',
        email='charlie@example.com'
    )

    print("\nUpdate user:")
    manager.dispatch(
        di,
        'user_updated',
        user_id=789,
        username='charlie',
        new_email='charlie.new@example.com'
    )

    print("\nDelete user:")
    manager.dispatch(
        di,
        'user_deleted',
        user_id=789,
        username='charlie'
    )


def complex_workflow():
    """Complex workflow with multiple handlers and events"""
    print("\n=== Complex Workflow ===")

    di = setup_di()
    manager = EventManager()

    # Setup complete event system
    manager.add_handler(
        'user_created',
        f'{__name__}.UserEventsHandler'
    )
    manager.add_handler(
        'user_created',
        f'{__name__}.NotificationHandler'
    )
    manager.add_handler(
        'user_created',
        f'{__name__}.AnalyticsHandler'
    )

    manager.add_handler(
        'user_deleted',
        f'{__name__}.UserEventsHandler'
    )
    manager.add_handler(
        'user_deleted',
        f'{__name__}.AnalyticsHandler'
    )

    # Simulate user lifecycle
    print("1. User Registration:")
    manager.dispatch(
        di,
        'user_created',
        user_id=999,
        username='dave',
        email='dave@example.com'
    )

    print("\n2. User Deletion:")
    manager.dispatch(
        di,
        'user_deleted',
        user_id=999,
        username='dave'
    )


if __name__ == '__main__':
    print("Class-based Event Handler Examples\n")
    single_handler()
    multiple_class_handlers()
    multiple_events_one_class()
    complex_workflow()
