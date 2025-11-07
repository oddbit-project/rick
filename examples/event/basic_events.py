"""
Basic event system examples

This example demonstrates:
- Creating an EventManager
- Registering handlers
- Dispatching events
- Function-based handlers
"""

from rick.base import Di
from rick.event import EventManager


# Function-based event handler
def welcome_user(event_name, user_id, username, **kwargs):
    """Simple function handler"""
    print(f"Event: {event_name}")
    print(f"  Welcome, {username}! Your ID is {user_id}")


def log_event(event_name, **kwargs):
    """Generic logging handler"""
    print(f"[LOG] Event '{event_name}' triggered")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


def send_notification(event_name, user_id, username, **kwargs):
    """Notification handler"""
    print(f"[NOTIFICATION] Sent to user {username}")


def simple_event():
    """Basic event dispatching"""
    print("=== Simple Event ===")

    di = Di()
    manager = EventManager()

    # Register a handler
    manager.add_handler('user_login', f'{__name__}.welcome_user')

    # Dispatch the event
    manager.dispatch(di, 'user_login', user_id=123, username='alice')


def multiple_handlers():
    """Multiple handlers for the same event"""
    print("\n=== Multiple Handlers ===")

    di = Di()
    manager = EventManager()

    # Register multiple handlers
    manager.add_handler('user_login', f'{__name__}.welcome_user')
    manager.add_handler('user_login', f'{__name__}.send_notification')
    manager.add_handler('user_login', f'{__name__}.log_event')

    # Dispatch - all handlers execute
    manager.dispatch(di, 'user_login', user_id=456, username='bob')


def multiple_events():
    """Different events with different handlers"""
    print("\n=== Multiple Events ===")

    di = Di()
    manager = EventManager()

    # Register handlers for different events
    manager.add_handler('user_login', f'{__name__}.welcome_user')
    manager.add_handler('user_logout', f'{__name__}.log_event')

    # Dispatch different events
    print("Login event:")
    manager.dispatch(di, 'user_login', user_id=789, username='charlie')

    print("\nLogout event:")
    manager.dispatch(di, 'user_logout', user_id=789, username='charlie')


def list_events():
    """List registered events"""
    print("\n=== List Events ===")

    manager = EventManager()

    # Register multiple events
    manager.add_handler('user_created', f'{__name__}.log_event')
    manager.add_handler('user_deleted', f'{__name__}.log_event')
    manager.add_handler('user_updated', f'{__name__}.log_event')

    # List all events
    events = manager.get_events()
    print(f"Registered events: {events}")


def remove_handler_example():
    """Remove handler from event"""
    print("\n=== Remove Handler ===")

    di = Di()
    manager = EventManager()

    # Register handlers
    manager.add_handler('user_login', f'{__name__}.welcome_user')
    manager.add_handler('user_login', f'{__name__}.log_event')

    print("With both handlers:")
    manager.dispatch(di, 'user_login', user_id=111, username='dave')

    # Remove one handler
    removed = manager.remove_handler(
        'user_login',
        f'{__name__}.log_event'
    )
    print(f"\nHandler removed: {removed}")

    print("\nWith only welcome_user handler:")
    manager.dispatch(di, 'user_login', user_id=111, username='dave')


def nonexistent_event():
    """Dispatching non-existent event"""
    print("\n=== Non-existent Event ===")

    di = Di()
    manager = EventManager()

    # Try to dispatch event that doesn't exist
    result = manager.dispatch(di, 'nonexistent_event', data='test')
    print(f"Event dispatched: {result}")  # Returns False


if __name__ == '__main__':
    print("Basic Event System Examples\n")
    simple_event()
    multiple_handlers()
    multiple_events()
    list_events()
    remove_handler_example()
    nonexistent_event()
