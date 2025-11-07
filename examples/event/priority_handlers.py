"""
Priority-based handler execution

This example demonstrates:
- Handler priority ordering
- Lower priority numbers execute first
- Using priorities to control execution order
- Practical priority grouping patterns
"""

from rick.base import Di
from rick.event import EventManager, EventHandler


class ValidationHandler(EventHandler):
    """High priority validation (runs first)"""

    def order_placed(self, order_id, amount, items):
        print(f"[PRIORITY 1] ValidationHandler.order_placed:")
        print(f"  Validating order {order_id}")
        print(f"  Amount: ${amount}, Items: {len(items)}")


class PaymentHandler(EventHandler):
    """Process payment after validation"""

    def order_placed(self, order_id, amount, items):
        print(f"[PRIORITY 10] PaymentHandler.order_placed:")
        print(f"  Processing payment for order {order_id}")
        print(f"  Charging ${amount}")


class InventoryHandler(EventHandler):
    """Update inventory after payment"""

    def order_placed(self, order_id, amount, items):
        print(f"[PRIORITY 20] InventoryHandler.order_placed:")
        print(f"  Updating inventory for order {order_id}")
        for item in items:
            print(f"    - {item}")


class NotificationHandler(EventHandler):
    """Send notifications after processing"""

    def order_placed(self, order_id, amount, items):
        print(f"[PRIORITY 50] NotificationHandler.order_placed:")
        print(f"  Sending confirmation for order {order_id}")


class AnalyticsHandler(EventHandler):
    """Track analytics last"""

    def order_placed(self, order_id, amount, items):
        print(f"[PRIORITY 100] AnalyticsHandler.order_placed:")
        print(f"  Tracking order {order_id} in analytics")


def simple_priority():
    """Simple priority demonstration"""
    print("=== Simple Priority ===")

    di = Di()
    manager = EventManager()

    # Register with different priorities
    # Lower number = higher priority (runs first)
    manager.add_handler(
        'user_action',
        f'{__name__}.handler_high',
        priority=1
    )
    manager.add_handler(
        'user_action',
        f'{__name__}.handler_medium',
        priority=50
    )
    manager.add_handler(
        'user_action',
        f'{__name__}.handler_low',
        priority=100
    )

    # Dispatch - handlers execute in priority order
    manager.dispatch(di, 'user_action', user='alice')


def handler_high(event_name, **kwargs):
    print(f"[PRIORITY 1] High priority handler executed")


def handler_medium(event_name, **kwargs):
    print(f"[PRIORITY 50] Medium priority handler executed")


def handler_low(event_name, **kwargs):
    print(f"[PRIORITY 100] Low priority handler executed")


def order_processing_pipeline():
    """Realistic order processing with priorities"""
    print("\n=== Order Processing Pipeline ===")

    di = Di()
    manager = EventManager()

    # Setup processing pipeline with priorities
    manager.add_handler(
        'order_placed',
        f'{__name__}.ValidationHandler',
        priority=1
    )
    manager.add_handler(
        'order_placed',
        f'{__name__}.PaymentHandler',
        priority=10
    )
    manager.add_handler(
        'order_placed',
        f'{__name__}.InventoryHandler',
        priority=20
    )
    manager.add_handler(
        'order_placed',
        f'{__name__}.NotificationHandler',
        priority=50
    )
    manager.add_handler(
        'order_placed',
        f'{__name__}.AnalyticsHandler',
        priority=100
    )

    # Process order - handlers execute in order
    manager.dispatch(
        di,
        'order_placed',
        order_id='ORD-123',
        amount=99.99,
        items=['Product A', 'Product B']
    )


def api_request_pipeline():
    """API request processing with priority groups"""
    print("\n=== API Request Pipeline ===")

    di = Di()
    manager = EventManager()

    # Priority groups:
    # 1-10: Authentication and security
    # 50-60: Business logic
    # 100+: Logging and analytics

    manager.add_handler(
        'api_request',
        f'{__name__}.auth_validator',
        priority=1
    )
    manager.add_handler(
        'api_request',
        f'{__name__}.permission_checker',
        priority=2
    )
    manager.add_handler(
        'api_request',
        f'{__name__}.request_processor',
        priority=50
    )
    manager.add_handler(
        'api_request',
        f'{__name__}.response_formatter',
        priority=51
    )
    manager.add_handler(
        'api_request',
        f'{__name__}.request_logger',
        priority=100
    )
    manager.add_handler(
        'api_request',
        f'{__name__}.analytics_tracker',
        priority=101
    )

    # Process API request
    manager.dispatch(
        di,
        'api_request',
        endpoint='/users',
        method='GET',
        user_id=123
    )


# API request handlers
def auth_validator(event_name, **kwargs):
    print(f"[PRIORITY 1] Validating authentication")


def permission_checker(event_name, **kwargs):
    print(f"[PRIORITY 2] Checking permissions")


def request_processor(event_name, **kwargs):
    print(f"[PRIORITY 50] Processing request")


def response_formatter(event_name, **kwargs):
    print(f"[PRIORITY 51] Formatting response")


def request_logger(event_name, **kwargs):
    print(f"[PRIORITY 100] Logging request")


def analytics_tracker(event_name, **kwargs):
    print(f"[PRIORITY 101] Tracking analytics")


def same_priority():
    """Multiple handlers with same priority"""
    print("\n=== Same Priority ===")

    di = Di()
    manager = EventManager()

    # Register multiple handlers with same priority
    # They execute in registration order
    manager.add_handler(
        'notification',
        f'{__name__}.handler_a',
        priority=50
    )
    manager.add_handler(
        'notification',
        f'{__name__}.handler_b',
        priority=50
    )
    manager.add_handler(
        'notification',
        f'{__name__}.handler_c',
        priority=50
    )

    manager.dispatch(di, 'notification', message='test')


def handler_a(event_name, **kwargs):
    print(f"[PRIORITY 50] Handler A")


def handler_b(event_name, **kwargs):
    print(f"[PRIORITY 50] Handler B")


def handler_c(event_name, **kwargs):
    print(f"[PRIORITY 50] Handler C")


def load_from_config():
    """Load handlers with priorities from configuration"""
    print("\n=== Load from Configuration ===")

    di = Di()
    manager = EventManager()

    # Configuration with priorities
    config = {
        'user_login': {
            1: [f'{__name__}.handler_high'],
            50: [f'{__name__}.handler_medium'],
            100: [f'{__name__}.handler_low']
        }
    }

    # Load configuration
    manager.load_handlers(config)

    # Dispatch
    manager.dispatch(di, 'user_login', username='bob')


if __name__ == '__main__':
    print("Priority-based Handler Execution Examples\n")
    simple_priority()
    order_processing_pipeline()
    api_request_pipeline()
    same_priority()
    load_from_config()
