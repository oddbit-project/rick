"""
State serialization examples

This example demonstrates:
- Saving event manager configuration
- Restoring event manager configuration
- Using sleep/wakeup for fast initialization
"""

from rick.base import Di
from rick.event import EventManager


def handler_a(event_name, **kwargs):
    print(f"Handler A: {event_name}")


def handler_b(event_name, **kwargs):
    print(f"Handler B: {event_name}")


def handler_c(event_name, **kwargs):
    print(f"Handler C: {event_name}")


def basic_serialization():
    """Basic save and restore"""
    print("=== Basic Serialization ===")

    # Create and configure manager
    manager1 = EventManager()
    manager1.add_handler('event1', f'{__name__}.handler_a')
    manager1.add_handler('event2', f'{__name__}.handler_b')
    manager1.add_handler('event3', f'{__name__}.handler_c')

    print(f"Manager 1 events: {manager1.get_events()}")

    # Save state
    state = manager1.sleep()
    print(f"State saved")

    # Create new manager and restore state
    manager2 = EventManager()
    manager2.wakeup(state)

    print(f"Manager 2 events: {manager2.get_events()}")
    print("State restored successfully!")


def preserve_priorities():
    """Priorities are preserved"""
    print("\n=== Preserve Priorities ===")

    di = Di()

    # Configure with priorities
    manager1 = EventManager()
    manager1.add_handler('test', f'{__name__}.handler_a', priority=1)
    manager1.add_handler('test', f'{__name__}.handler_b', priority=50)
    manager1.add_handler('test', f'{__name__}.handler_c', priority=100)

    print("Original manager:")
    manager1.dispatch(di, 'test')

    # Save and restore
    state = manager1.sleep()
    manager2 = EventManager()
    manager2.wakeup(state)

    print("\nRestored manager:")
    manager2.dispatch(di, 'test')


def fast_initialization():
    """Fast initialization pattern"""
    print("\n=== Fast Initialization ===")

    # Expensive initial setup (happens once)
    print("1. Initial setup (slow)...")
    manager = EventManager()

    # Register many handlers
    for i in range(10):
        manager.add_handler(
            f'event_{i}',
            f'{__name__}.handler_a'
        )

    print(f"   Registered {len(manager.get_events())} events")

    # Save configuration
    state = manager.sleep()
    print("2. State saved")

    # Fast subsequent initialization
    print("3. Fast initialization (quick)...")
    new_manager = EventManager()
    new_manager.wakeup(state)
    print(f"   Restored {len(new_manager.get_events())} events")


def state_sharing():
    """Share configuration between managers"""
    print("\n=== State Sharing ===")

    # Create template configuration
    template = EventManager()
    template.add_handler('user_login', f'{__name__}.handler_a')
    template.add_handler('user_logout', f'{__name__}.handler_b')
    template.add_handler('data_updated', f'{__name__}.handler_c')

    # Save template
    template_state = template.sleep()

    # Create multiple managers from same template
    managers = []
    for i in range(3):
        mgr = EventManager()
        mgr.wakeup(template_state)
        managers.append(mgr)
        print(f"Manager {i+1} events: {mgr.get_events()}")

    print(f"Created {len(managers)} managers from template")


def configuration_backup():
    """Use for configuration backup"""
    print("\n=== Configuration Backup ===")

    manager = EventManager()

    # Add some handlers
    manager.add_handler('event1', f'{__name__}.handler_a')
    manager.add_handler('event2', f'{__name__}.handler_b')

    print(f"Original configuration: {manager.get_events()}")

    # Backup configuration
    backup = manager.sleep()

    # Modify configuration
    manager.add_handler('event3', f'{__name__}.handler_c')
    manager.remove_handler('event1', f'{__name__}.handler_a')

    print(f"Modified configuration: {manager.get_events()}")

    # Restore from backup
    manager.wakeup(backup)

    print(f"Restored configuration: {manager.get_events()}")


def multiple_configurations():
    """Switch between different configurations"""
    print("\n=== Multiple Configurations ===")

    manager = EventManager()

    # Configuration A: User events
    manager.add_handler('user_login', f'{__name__}.handler_a')
    manager.add_handler('user_logout', f'{__name__}.handler_b')
    config_a = manager.sleep()
    print(f"Config A: {manager.get_events()}")

    # Clear and create Configuration B: Data events
    manager.purge()
    manager.add_handler('data_create', f'{__name__}.handler_a')
    manager.add_handler('data_update', f'{__name__}.handler_b')
    manager.add_handler('data_delete', f'{__name__}.handler_c')
    config_b = manager.sleep()
    print(f"Config B: {manager.get_events()}")

    # Switch back to config A
    manager.wakeup(config_a)
    print(f"Switched to Config A: {manager.get_events()}")

    # Switch to config B
    manager.wakeup(config_b)
    print(f"Switched to Config B: {manager.get_events()}")


if __name__ == '__main__':
    print("State Serialization Examples\n")
    basic_serialization()
    preserve_priorities()
    fast_initialization()
    state_sharing()
    configuration_backup()
    multiple_configurations()
