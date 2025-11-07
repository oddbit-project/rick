# Event System

Rick provides a flexible event system for building event-driven applications. The event system allows you to define
events, register handlers, and dispatch events with priority-based execution.

## Overview

The event system consists of three main components:

- **EventManager** - Central event dispatcher and registry
- **EventHandler** - Base class for event handler classes
- **EventState** - Serialization wrapper for saving/restoring event configuration

## Key Features

- **Priority-based Execution** - Handlers execute in order of priority (lower numbers first)
- **Thread-safe** - Safe for concurrent event registration and dispatching
- **Flexible Handlers** - Support both class-based and function-based handlers
- **Circular Dependency Detection** - Prevents infinite event loops
- **DI Integration** - Handlers receive dependency injection container
- **State Serialization** - Save and restore event configuration for fast initialization

## Quick Start

### Basic Event Dispatching

```python
from rick.base import Di
from rick.event import EventManager, EventHandler

# Create DI container and event manager
di = Di()
manager = EventManager()


# Define event handler class
class UserHandler(EventHandler):
    def user_created(self, user_id, username):
        print(f"User created: {username} (ID: {user_id})")
        # Access DI container
        logger = self.get_di().get('logger')


# Register handler
manager.add_handler('user_created', 'myapp.handlers.UserHandler', priority=100)

# Dispatch event
manager.dispatch(di, 'user_created', user_id=123, username='alice')
```

### Function-based Handlers

```python
from rick.event import EventManager

manager = EventManager()


# Define handler function
def notify_admin(event_name, **kwargs):
    print(f"Event: {event_name}")
    print(f"Data: {kwargs}")


# Register function handler
manager.add_handler('user_login', 'myapp.handlers.notify_admin')

# Dispatch event
manager.dispatch(di, 'user_login', username='bob', ip='192.168.1.1')
```

## Event Manager

### Creating Event Manager

```python
from rick.event import EventManager

manager = EventManager()
```

### Registering Handlers

#### Single Handler

```python
# Register class-based handler
manager.add_handler('order_placed', 'myapp.orders.OrderHandler', priority=10)

# Register function-based handler
manager.add_handler('order_placed', 'myapp.notifications.send_email', priority=20)
```

#### Multiple Handlers from Configuration

```python
config = {
    'user_created': {
        10: ['myapp.handlers.ValidateUser', 'myapp.handlers.SendWelcomeEmail'],
        20: ['myapp.analytics.TrackUser']
    },
    'order_placed': {
        10: ['myapp.orders.ProcessPayment'],
        20: ['myapp.orders.SendConfirmation', 'myapp.inventory.UpdateStock']
    }
}

manager.load_handlers(config)
```

### Dispatching Events

```python
from rick.base import Di

di = Di()
manager = EventManager()

# Register handlers
manager.add_handler('payment_failed', 'myapp.handlers.PaymentHandler')

# Dispatch with keyword arguments
success = manager.dispatch(
    di,
    'payment_failed',
    order_id='ORD-123',
    amount=99.99,
    reason='Insufficient funds'
)

# Returns True if event exists and was dispatched, False otherwise
if success:
    print("Event dispatched")
```

### Managing Handlers

#### Remove Handler

```python
# Remove specific handler from event
removed = manager.remove_handler('user_login', 'myapp.handlers.LoginHandler')

if removed:
    print("Handler removed")
else:
    print("Handler not found")
```

#### List Events

```python
# Get all registered event names
events = manager.get_events()
print(f"Registered events: {events}")
```

#### Clear All Events

```python
# Remove all events and handlers
manager.purge()
```

## Event Handlers

### Class-based Handlers

Event handler classes must:

1. Extend `EventHandler`
2. Define methods matching event names
3. Accept keyword arguments matching event data

```python
from rick.event import EventHandler


class UserEventsHandler(EventHandler):
    def user_created(self, user_id, username, email):
        """Handle user creation"""
        logger = self.get_di().get('logger')
        logger.info(f"New user: {username} ({email})")

        # Perform additional actions
        db = self.get_di().get('database')
        db.log_event('user_created', user_id)

    def user_deleted(self, user_id, username):
        """Handle user deletion"""
        cache = self.get_di().get('cache')
        cache.delete(f"user:{user_id}")
```

### Function-based Handlers

Function handlers must:

1. Accept `event_name` keyword argument
2. Accept additional keyword arguments for event data

```python
def audit_logger(event_name, **kwargs):
    """Generic audit logging handler"""
    print(f"[AUDIT] Event: {event_name}")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


def send_notification(event_name, user_id, message, **kwargs):
    """Send notification to user"""
    notification_service = get_notification_service()
    notification_service.send(user_id, message)
```

### Handler Priority

Handlers with lower priority numbers execute first:

```python
manager = EventManager()

# These execute in order: 1, 10, 20, 100
manager.add_handler('user_login', 'myapp.auth.ValidateSession', priority=1)
manager.add_handler('user_login', 'myapp.auth.UpdateLastSeen', priority=10)
manager.add_handler('user_login', 'myapp.analytics.TrackLogin', priority=20)
manager.add_handler('user_login', 'myapp.logs.LogActivity', priority=100)
```

## State Serialization

Save and restore event configuration for fast initialization:

```python
from rick.event import EventManager

# Configure event manager
manager = EventManager()
manager.add_handler('user_created', 'myapp.handlers.UserHandler')
manager.add_handler('order_placed', 'myapp.handlers.OrderHandler')

# Serialize configuration
state = manager.sleep()

# Later, create new manager and restore state
new_manager = EventManager()
new_manager.wakeup(state)

# New manager has same handlers
print(new_manager.get_events())  # ['user_created', 'order_placed']
```

## Advanced Usage

### Multi-Priority Handlers

Register multiple handlers at different priorities for fine-grained control:

```python
manager = EventManager()

# Authentication and validation (high priority)
manager.add_handler('api_request', 'myapp.auth.ValidateToken', priority=1)
manager.add_handler('api_request', 'myapp.auth.CheckPermissions', priority=2)

# Business logic (medium priority)
manager.add_handler('api_request', 'myapp.api.ProcessRequest', priority=50)
manager.add_handler('api_request', 'myapp.api.TransformResponse', priority=51)

# Logging and analytics (low priority)
manager.add_handler('api_request', 'myapp.logs.LogRequest', priority=100)
manager.add_handler('api_request', 'myapp.analytics.TrackUsage', priority=101)
```

### Dependency Injection in Handlers

Handlers can access services from the DI container:

```python
from rick.event import EventHandler


class EmailHandler(EventHandler):
    def send_welcome_email(self, user_id, email, username):
        # Get services from DI container
        mailer = self.get_di().get('mailer')
        template_engine = self.get_di().get('templates')
        config = self.get_di().get('config')

        # Use services
        html = template_engine.render('welcome.html', username=username)
        mailer.send(
            to=email,
            subject=config['welcome_subject'],
            body=html
        )
```

### Error Handling

The event system raises `RuntimeError` for:

- Circular event dependencies
- Missing handler modules or classes
- Invalid handler types
- Duplicate handler registration

```python
from rick.event import EventManager

manager = EventManager()

try:
    manager.add_handler('test_event', 'myapp.InvalidHandler')
    manager.dispatch(di, 'test_event')
except RuntimeError as e:
    print(f"Event error: {e}")
```

### Thread Safety

The EventManager is thread-safe for concurrent operations:

```python
import threading
from rick.event import EventManager

manager = EventManager()


def register_handlers():
    for i in range(100):
        manager.add_handler(f'event_{i}', f'myapp.Handler{i}', priority=i)


# Multiple threads can safely register handlers
threads = [threading.Thread(target=register_handlers) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Common Patterns

### Event-Driven Architecture

```python
from rick.base import Di
from rick.event import EventManager, EventHandler

# Setup
di = Di()
di.add('database', create_database())
di.add('cache', create_cache())
di.add('mailer', create_mailer())

manager = EventManager()
manager.add_handler('user_registered', 'myapp.users.UserEventsHandler', priority=10)
manager.add_handler('user_registered', 'myapp.emails.WelcomeEmailHandler', priority=20)
manager.add_handler('user_registered', 'myapp.analytics.TrackingHandler', priority=30)


# User registration
def register_user(username, email, password):
    user_id = create_user_in_db(username, email, password)

    # Dispatch event - handlers take care of the rest
    manager.dispatch(
        di,
        'user_registered',
        user_id=user_id,
        username=username,
        email=email
    )

    return user_id
```

### Decoupled Components

```python
# Authentication module
class AuthHandler(EventHandler):
    def user_login(self, user_id, username):
        self.get_di().get('session').create(user_id)


# Analytics module (separate concern)
class AnalyticsHandler(EventHandler):
    def user_login(self, user_id, username):
        self.get_di().get('analytics').track('login', user_id)


# Notification module (separate concern)
class NotificationHandler(EventHandler):
    def user_login(self, user_id, username):
        self.get_di().get('notifications').send(user_id, 'Login detected')


# Each module handles its own concerns independently
manager.add_handler('user_login', 'myapp.auth.AuthHandler', priority=10)
manager.add_handler('user_login', 'myapp.analytics.AnalyticsHandler', priority=20)
manager.add_handler('user_login', 'myapp.notifications.NotificationHandler', priority=30)
```

### Plugin System

```python
# Define plugin interface
class Plugin(EventHandler):
    pass


# Load plugins dynamically
plugins = [
    'plugins.spam_filter.SpamFilterPlugin',
    'plugins.auto_tag.AutoTagPlugin',
    'plugins.sentiment.SentimentPlugin'
]

for plugin in plugins:
    manager.add_handler('message_received', plugin, priority=50)

# Dispatch to all plugins
manager.dispatch(di, 'message_received', message_id=123, content='Hello')
```

### Audit Trail

```python
def audit_trail(event_name, **kwargs):
    """Log all events for audit purposes"""
    timestamp = datetime.now()
    user_id = kwargs.get('user_id', 'system')

    audit_db = get_audit_database()
    audit_db.insert({
        'timestamp': timestamp,
        'event': event_name,
        'user_id': user_id,
        'data': kwargs
    })


# Register audit handler for all events
for event in ['user_login', 'user_logout', 'data_modified', 'admin_action']:
    manager.add_handler(event, 'myapp.audit.audit_trail', priority=999)
```

## API Reference

### EventManager

#### Methods

**`add_handler(event_name: str, handler: str, priority: int = 100)`**

Register an event handler.

- **event_name** - Name of the event
- **handler** - Fully qualified class or function name (e.g., 'myapp.handlers.UserHandler')
- **priority** - Execution priority (lower numbers execute first, default 100)
- **Raises** - RuntimeError if handler is invalid or already registered

**`remove_handler(event_name: str, handler: str) -> bool`**

Remove a handler from an event.

- **Returns** - True if handler was removed, False if not found

**`load_handlers(src: dict)`**

Load multiple handlers from configuration dictionary.

- **src** - Configuration dict with format:
  ```python
  {
      'event_name': {
          priority: ['handler1', 'handler2'],
          priority2: ['handler3']
      }
  }
  ```

**`dispatch(di: Di, event_name: str, **kwargs) -> bool`**

Dispatch an event to all registered handlers.

- **di** - Dependency injection container
- **event_name** - Event to dispatch
- **kwargs** - Event data passed to handlers
- **Returns** - True if event was dispatched, False if event doesn't exist
- **Raises** - RuntimeError on circular dependencies or handler errors

**`get_events() -> list`**

Get list of all registered event names.

**`purge()`**

Remove all events and handlers.

**`sleep() -> EventState`**

Serialize event configuration.

**`wakeup(src: EventState)`**

Restore event configuration.

### EventHandler

Base class for event handler classes.

**`__init__(di: Di)`**

Initialize handler with DI container.

**`get_di() -> Di`**

Get dependency injection container.

**`set_di(di: Di)`**

Set dependency injection container.

### EventState

Serialization wrapper for EventManager configuration.

**`__init__(src: dict)`**

Create state from configuration dictionary.

**Attributes:**

- **data** - Configuration dictionary (treat as read-only)

## Best Practices

1. **Use Priority Wisely** - Group related priorities (1-10 for validation, 50-60 for business logic, 100+ for logging)

2. **Keep Handlers Focused** - Each handler should do one thing well

3. **Avoid Side Effects in Handlers** - Handlers should be predictable and testable

4. **Use DI Container** - Store shared services in DI container rather than global state

5. **Handle Errors Gracefully** - Catch exceptions in handlers to prevent event chain disruption

6. **Document Events** - Maintain documentation of event names and their data structure

7. **Test Event Flow** - Write integration tests that verify event dispatching works correctly

8. **Use Consistent Naming** - Use clear, descriptive event names (e.g., 'user_created', not 'usr_new')

## Examples

Complete working examples are available in `examples/event/`:

- **basic_events.py** - Simple event dispatching
- **priority_handlers.py** - Priority-based execution
- **class_handlers.py** - Using EventHandler classes
- **function_handlers.py** - Function-based handlers
- **state_serialization.py** - Saving and restoring event configuration

Run examples:

```bash
python examples/event/basic_events.py
```

## See Also

- **Dependency Injection** - Rick's DI container (`rick.base.Di`)
- **Injectable Mixin** - Base class for DI-aware components (`rick.mixin.Injectable`)
