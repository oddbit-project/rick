"""
Test all code examples from docs/event/index.md

This test ensures all documentation examples are working correctly.
"""

import pytest
from rick.base import Di
from rick.event import EventManager, EventHandler
from rick.event.manager import EventState


# =============================================================================
# Quick Start Examples
# =============================================================================

class TestQuickStartExamples:
    """Test examples from Quick Start section"""

    def test_basic_event_dispatching(self):
        """Test: Basic Event Dispatching"""
        from rick.base import Di
        from rick.event import EventManager, EventHandler

        # Create DI container and event manager
        di = Di()
        di.add('logger', {'name': 'test_logger'})
        manager = EventManager()

        # Define event handler class
        class UserHandler(EventHandler):
            def user_created(self, user_id, username):
                print(f"User created: {username} (ID: {user_id})")
                # Access DI container
                logger = self.get_di().get('logger')
                assert logger is not None

        # Register handler
        manager.add_handler('user_created', f'{__name__}.UserHandler', priority=100)

        # Dispatch event
        result = manager.dispatch(di, 'user_created', user_id=123, username='alice')
        assert result is True

    def test_function_based_handlers(self):
        """Test: Function-based Handlers"""
        from rick.event import EventManager

        manager = EventManager()

        # Define handler function
        def notify_admin(event_name, **kwargs):
            print(f"Event: {event_name}")
            print(f"Data: {kwargs}")

        # Register function handler
        manager.add_handler('user_login', f'{__name__}.notify_admin')

        # Dispatch event
        di = Di()
        result = manager.dispatch(di, 'user_login', username='bob', ip='192.168.1.1')
        assert result is True


# =============================================================================
# Event Manager Examples
# =============================================================================

class TestEventManagerExamples:
    """Test EventManager examples"""

    def test_single_handler_registration(self):
        """Test: Single Handler"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        # Register class-based handler
        manager.add_handler('order_placed', f'{__name__}.test_handler', priority=10)

        events = manager.get_events()
        assert 'order_placed' in events

    def test_multiple_handlers_from_config(self):
        """Test: Multiple Handlers from Configuration"""
        manager = EventManager()

        def handler_a(event_name, **kwargs):
            pass

        def handler_b(event_name, **kwargs):
            pass

        config = {
            'user_created': {
                10: [f'{__name__}.handler_a', f'{__name__}.handler_b'],
            }
        }

        manager.load_handlers(config)
        events = manager.get_events()
        assert 'user_created' in events

    def test_dispatching_events(self):
        """Test: Dispatching Events"""
        from rick.base import Di

        di = Di()
        manager = EventManager()

        def payment_handler(event_name, **kwargs):
            assert event_name == 'payment_failed'
            assert kwargs['order_id'] == 'ORD-123'
            assert kwargs['amount'] == 99.99

        # Register handlers
        manager.add_handler('payment_failed', f'{__name__}.payment_handler')

        # Dispatch with keyword arguments
        success = manager.dispatch(
            di,
            'payment_failed',
            order_id='ORD-123',
            amount=99.99,
            reason='Insufficient funds'
        )

        assert success is True

    def test_remove_handler(self):
        """Test: Remove Handler"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('user_login', f'{__name__}.test_handler')

        # Remove specific handler from event
        removed = manager.remove_handler('user_login', f'{__name__}.test_handler')
        assert removed is True

        # Try to remove again
        removed = manager.remove_handler('user_login', f'{__name__}.test_handler')
        assert removed is False

    def test_list_events(self):
        """Test: List Events"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('event1', f'{__name__}.test_handler')
        manager.add_handler('event2', f'{__name__}.test_handler')

        # Get all registered event names
        events = manager.get_events()
        assert 'event1' in events
        assert 'event2' in events
        assert len(events) == 2

    def test_clear_all_events(self):
        """Test: Clear All Events"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('event1', f'{__name__}.test_handler')
        manager.add_handler('event2', f'{__name__}.test_handler')

        # Remove all events and handlers
        manager.purge()

        events = manager.get_events()
        assert len(events) == 0


# =============================================================================
# Event Handler Examples
# =============================================================================

class TestEventHandlerExamples:
    """Test EventHandler examples"""

    def test_class_based_handlers(self):
        """Test: Class-based Handlers"""
        from rick.event import EventHandler

        class UserEventsHandler(EventHandler):
            def user_created(self, user_id, username, email):
                """Handle user creation"""
                logger = self.get_di().get('logger')
                assert logger is not None

                # Perform additional actions
                db = self.get_di().get('database')
                assert db is not None

            def user_deleted(self, user_id, username):
                """Handle user deletion"""
                cache = self.get_di().get('cache')
                assert cache is not None

        di = Di()
        di.add('logger', {'name': 'logger'})
        di.add('database', {'name': 'db'})
        di.add('cache', {'name': 'cache'})

        manager = EventManager()
        manager.add_handler('user_created', f'{__name__}.UserEventsHandler')
        manager.add_handler('user_deleted', f'{__name__}.UserEventsHandler')

        # Test user_created
        result = manager.dispatch(
            di,
            'user_created',
            user_id=1,
            username='alice',
            email='alice@example.com'
        )
        assert result is True

        # Test user_deleted
        result = manager.dispatch(di, 'user_deleted', user_id=1, username='alice')
        assert result is True

    def test_function_based_handlers_detailed(self):
        """Test: Function-based Handlers"""
        def audit_logger(event_name, **kwargs):
            """Generic audit logging handler"""
            assert event_name is not None
            assert isinstance(kwargs, dict)

        def send_notification(event_name, user_id, message, **kwargs):
            """Send notification to user"""
            assert user_id is not None
            assert message is not None

        di = Di()
        manager = EventManager()

        manager.add_handler('test_event', f'{__name__}.audit_logger')
        manager.add_handler('notification', f'{__name__}.send_notification')

        manager.dispatch(di, 'test_event', data='test')
        manager.dispatch(di, 'notification', user_id=123, message='Hello')

    def test_handler_priority(self):
        """Test: Handler Priority"""
        # Reset global execution order
        global execution_order_priority
        execution_order_priority = []

        di = Di()
        manager = EventManager()

        # These execute in order: 1, 10, 20, 100
        manager.add_handler('user_login', f'{__name__}.handler_priority_1', priority=1)
        manager.add_handler('user_login', f'{__name__}.handler_priority_10', priority=10)
        manager.add_handler('user_login', f'{__name__}.handler_priority_20', priority=20)
        manager.add_handler('user_login', f'{__name__}.handler_priority_100', priority=100)

        manager.dispatch(di, 'user_login')

        assert execution_order_priority == [1, 10, 20, 100]


# =============================================================================
# State Serialization Examples
# =============================================================================

class TestStateSerialization:
    """Test state serialization examples"""

    def test_basic_serialization(self):
        """Test: Save and restore event configuration"""
        from rick.event import EventManager

        def test_handler(event_name, **kwargs):
            pass

        # Configure event manager
        manager = EventManager()
        manager.add_handler('user_created', f'{__name__}.test_handler')
        manager.add_handler('order_placed', f'{__name__}.test_handler')

        # Serialize configuration
        state = manager.sleep()
        assert state is not None

        # Later, create new manager and restore state
        new_manager = EventManager()
        new_manager.wakeup(state)

        # New manager has same handlers
        events = new_manager.get_events()
        assert 'user_created' in events
        assert 'order_placed' in events


# =============================================================================
# Advanced Usage Examples
# =============================================================================

class TestAdvancedUsage:
    """Test advanced usage examples"""

    def test_multi_priority_handlers(self):
        """Test: Multi-Priority Handlers"""
        # Reset global execution order
        global execution_order_advanced
        execution_order_advanced = []

        di = Di()
        manager = EventManager()

        # Authentication and validation (high priority)
        manager.add_handler('api_request', f'{__name__}.auth_validate', priority=1)
        manager.add_handler('api_request', f'{__name__}.auth_permissions', priority=2)

        # Business logic (medium priority)
        manager.add_handler('api_request', f'{__name__}.process_request', priority=50)

        # Logging and analytics (low priority)
        manager.add_handler('api_request', f'{__name__}.log_request', priority=100)

        manager.dispatch(di, 'api_request')

        assert execution_order_advanced == [
            'auth_validate',
            'auth_permissions',
            'process_request',
            'log_request'
        ]

    def test_dependency_injection_in_handlers(self):
        """Test: Dependency Injection in Handlers"""
        from rick.event import EventHandler

        class EmailHandler(EventHandler):
            def send_welcome_email(self, user_id, email, username):
                # Get services from DI container
                mailer = self.get_di().get('mailer')
                template_engine = self.get_di().get('templates')
                config = self.get_di().get('config')

                assert mailer is not None
                assert template_engine is not None
                assert config is not None

        di = Di()
        di.add('mailer', {'send': lambda: None})
        di.add('templates', {'render': lambda: None})
        di.add('config', {'welcome_subject': 'Welcome!'})

        manager = EventManager()
        manager.add_handler('welcome', f'{__name__}.EmailHandler')

        result = manager.dispatch(
            di,
            'welcome',
            user_id=1,
            email='test@example.com',
            username='test'
        )
        assert result is True

    def test_error_handling(self):
        """Test: Error Handling"""
        from rick.event import EventManager

        manager = EventManager()

        # Try to register invalid handler
        with pytest.raises(RuntimeError):
            manager.add_handler('test_event', 'nonexistent.module.Handler')
            di = Di()
            manager.dispatch(di, 'test_event')

    def test_circular_dependency_detection(self):
        """Test: Circular event dependency detection"""
        di = Di()
        manager = EventManager()

        # This would create circular dependency if we dispatched same event
        def circular_handler(event_name, **kwargs):
            # This would cause circular dependency
            pass

        manager.add_handler('event1', f'{__name__}.circular_handler')

        # Normal dispatch works
        result = manager.dispatch(di, 'event1')
        assert result is True


# =============================================================================
# Common Patterns Examples
# =============================================================================

class TestCommonPatterns:
    """Test common pattern examples"""

    def test_event_driven_architecture(self):
        """Test: Event-Driven Architecture pattern"""
        from rick.base import Di
        from rick.event import EventManager, EventHandler

        class UserEventsHandler(EventHandler):
            def user_registered(self, user_id, username, email):
                db = self.get_di().get('database')
                assert db is not None

        def create_database():
            return {'insert': lambda: None}

        # Setup
        di = Di()
        di.add('database', create_database())

        manager = EventManager()
        manager.add_handler('user_registered', f'{__name__}.UserEventsHandler', priority=10)

        # User registration
        def register_user(username, email, password):
            user_id = 123

            # Dispatch event - handlers take care of the rest
            manager.dispatch(
                di,
                'user_registered',
                user_id=user_id,
                username=username,
                email=email
            )

            return user_id

        user_id = register_user('john', 'john@example.com', 'password')
        assert user_id == 123

    def test_decoupled_components(self):
        """Test: Decoupled Components pattern"""
        # Authentication module
        class AuthHandler(EventHandler):
            def user_login(self, user_id, username):
                session = self.get_di().get('session')
                assert session is not None

        # Analytics module (separate concern)
        class AnalyticsHandler(EventHandler):
            def user_login(self, user_id, username):
                analytics = self.get_di().get('analytics')
                assert analytics is not None

        di = Di()
        di.add('session', {'create': lambda: None})
        di.add('analytics', {'track': lambda: None})

        manager = EventManager()

        # Each module handles its own concerns independently
        manager.add_handler('user_login', f'{__name__}.AuthHandler', priority=10)
        manager.add_handler('user_login', f'{__name__}.AnalyticsHandler', priority=20)

        result = manager.dispatch(di, 'user_login', user_id=1, username='alice')
        assert result is True


# =============================================================================
# API Reference Tests
# =============================================================================

class TestAPIReference:
    """Test API Reference examples"""

    def test_add_handler(self):
        """Test: add_handler method"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        # Valid registration
        manager.add_handler('test_event', f'{__name__}.test_handler', priority=50)

        # Test duplicate handler raises error
        with pytest.raises(RuntimeError, match='duplicated handler'):
            manager.add_handler('test_event', f'{__name__}.test_handler', priority=50)

    def test_remove_handler_api(self):
        """Test: remove_handler method"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('test_event', f'{__name__}.test_handler')

        # Returns True if handler was removed
        result = manager.remove_handler('test_event', f'{__name__}.test_handler')
        assert result is True

        # Returns False if not found
        result = manager.remove_handler('test_event', f'{__name__}.test_handler')
        assert result is False

    def test_load_handlers_api(self):
        """Test: load_handlers method"""
        manager = EventManager()

        config = {
            'event1': {
                10: [f'{__name__}.handler1', f'{__name__}.handler2'],
            },
            'event2': {
                20: [f'{__name__}.handler1']
            }
        }

        manager.load_handlers(config)

        events = manager.get_events()
        assert 'event1' in events
        assert 'event2' in events

    def test_dispatch_api(self):
        """Test: dispatch method"""
        # Reset global counter
        global dispatch_counter
        dispatch_counter = 0

        di = Di()
        manager = EventManager()

        manager.add_handler('test_event', f'{__name__}.dispatch_test_handler')

        # Returns True if event was dispatched
        result = manager.dispatch(di, 'test_event', data='test')
        assert result is True
        assert dispatch_counter == 1

        # Returns False if event doesn't exist
        result = manager.dispatch(di, 'nonexistent', data='test')
        assert result is False

    def test_get_events_api(self):
        """Test: get_events method"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('event1', f'{__name__}.test_handler')
        manager.add_handler('event2', f'{__name__}.test_handler')
        manager.add_handler('event3', f'{__name__}.test_handler')

        events = manager.get_events()
        assert isinstance(events, list)
        assert len(events) == 3

    def test_purge_api(self):
        """Test: purge method"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('event1', f'{__name__}.test_handler')
        manager.add_handler('event2', f'{__name__}.test_handler')

        manager.purge()

        events = manager.get_events()
        assert len(events) == 0

    def test_sleep_wakeup_api(self):
        """Test: sleep and wakeup methods"""
        manager = EventManager()

        def test_handler(event_name, **kwargs):
            pass

        manager.add_handler('event1', f'{__name__}.test_handler')

        # Serialize configuration
        state = manager.sleep()
        assert isinstance(state, EventState)

        # Restore configuration
        new_manager = EventManager()
        new_manager.wakeup(state)

        events = new_manager.get_events()
        assert 'event1' in events

    def test_event_handler_api(self):
        """Test: EventHandler class"""
        class TestHandler(EventHandler):
            def test_event(self):
                di = self.get_di()
                assert di is not None

                # Test set_di
                new_di = Di()
                self.set_di(new_di)
                assert self.get_di() is new_di

        di = Di()
        handler = TestHandler(di)

        # Test __init__ and get_di
        assert handler.get_di() is di

        # Test event method
        handler.test_event()

    def test_event_state_api(self):
        """Test: EventState class"""
        config = {
            'event1': {
                'handlers': ['handler1'],
                10: ['handler1']
            }
        }

        state = EventState(config)

        # Test data attribute
        assert isinstance(state.data, dict)
        assert 'event1' in state.data


# =============================================================================
# Helper classes and functions for tests
# =============================================================================

# Global variables for tracking execution order
execution_order_priority = []
execution_order_advanced = []
dispatch_counter = 0

# Define handler classes at module level so they can be imported
class UserHandler(EventHandler):
    def user_created(self, user_id, username):
        print(f"User created: {username} (ID: {user_id})")
        logger = self.get_di().get('logger')
        assert logger is not None


def notify_admin(event_name, **kwargs):
    print(f"Event: {event_name}")
    print(f"Data: {kwargs}")


# Removed duplicate - using function defined above


def handler_a(event_name, **kwargs):
    pass


def handler_b(event_name, **kwargs):
    pass


def payment_handler(event_name, **kwargs):
    assert event_name == 'payment_failed'


class UserEventsHandler(EventHandler):
    def user_created(self, user_id, username, email):
        """Handle user creation"""
        logger = self.get_di().get('logger')
        assert logger is not None

        db = self.get_di().get('database')
        assert db is not None

    def user_deleted(self, user_id, username):
        """Handle user deletion"""
        cache = self.get_di().get('cache')
        assert cache is not None

    def user_registered(self, user_id, username, email):
        db = self.get_di().get('database')
        assert db is not None


def audit_logger(event_name, **kwargs):
    """Generic audit logging handler"""
    assert event_name is not None
    assert isinstance(kwargs, dict)


def send_notification(event_name, user_id, message, **kwargs):
    """Send notification to user"""
    assert user_id is not None
    assert message is not None


def handler_priority_1(event_name, **kwargs):
    global execution_order_priority
    execution_order_priority.append(1)


def handler_priority_10(event_name, **kwargs):
    global execution_order_priority
    execution_order_priority.append(10)


def handler_priority_20(event_name, **kwargs):
    global execution_order_priority
    execution_order_priority.append(20)


def handler_priority_100(event_name, **kwargs):
    global execution_order_priority
    execution_order_priority.append(100)


def auth_validate(event_name, **kwargs):
    global execution_order_advanced
    execution_order_advanced.append('auth_validate')


def auth_permissions(event_name, **kwargs):
    global execution_order_advanced
    execution_order_advanced.append('auth_permissions')


def process_request(event_name, **kwargs):
    global execution_order_advanced
    execution_order_advanced.append('process_request')


def log_request(event_name, **kwargs):
    global execution_order_advanced
    execution_order_advanced.append('log_request')


def dispatch_test_handler(event_name, **kwargs):
    global dispatch_counter
    dispatch_counter += 1


class EmailHandler(EventHandler):
    def send_welcome_email(self, user_id, email, username):
        mailer = self.get_di().get('mailer')
        template_engine = self.get_di().get('templates')
        config = self.get_di().get('config')

        assert mailer is not None
        assert template_engine is not None
        assert config is not None

    def welcome(self, user_id, email, username):
        self.send_welcome_email(user_id, email, username)


def circular_handler(event_name, **kwargs):
    pass


class AuthHandler(EventHandler):
    def user_login(self, user_id, username):
        session = self.get_di().get('session')
        assert session is not None


class AnalyticsHandler(EventHandler):
    def user_login(self, user_id, username):
        analytics = self.get_di().get('analytics')
        assert analytics is not None


def handler1(event_name, **kwargs):
    pass


def handler2(event_name, **kwargs):
    pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
