# Event System Examples

This directory contains comprehensive examples demonstrating Rick's event system.

## Examples

### basic_events.py

Basic event system functionality:
- Simple event dispatching
- Function-based handlers
- Multiple handlers for same event
- Managing different events
- Removing handlers

```bash
python examples/event/basic_events.py
```

### class_handlers.py

Class-based event handlers:
- Creating EventHandler classes
- Accessing DI container in handlers
- Multiple event methods in one class
- Complex workflows with multiple handlers
- Using services from DI container

```bash
python examples/event/class_handlers.py
```

### priority_handlers.py

Priority-based handler execution:
- Handler priority ordering
- Lower priority numbers execute first
- Practical priority grouping patterns
- Order processing pipeline
- API request pipeline

```bash
python examples/event/priority_handlers.py
```

### state_serialization.py

State serialization and restoration:
- Saving event manager configuration
- Restoring configuration
- Fast initialization pattern
- Configuration backup and restore
- Switching between configurations

```bash
python examples/event/state_serialization.py
```

## Running All Examples

```bash
for file in examples/event/*.py; do
    if [[ "$file" != *"README"* ]]; then
        echo "=== Testing $file ==="
        python "$file"
        echo ""
    fi
done
```

## Key Concepts

### EventManager

Central event dispatcher and registry:
- `add_handler(event_name, handler, priority)` - Register handler
- `dispatch(di, event_name, **kwargs)` - Dispatch event
- `remove_handler(event_name, handler)` - Remove handler
- `get_events()` - List registered events
- `sleep()` / `wakeup()` - Save/restore configuration

### EventHandler

Base class for event handler classes:
- Extend EventHandler
- Define methods matching event names
- Access DI container via `get_di()`

### Handler Types

**Function Handlers:**
```python
def my_handler(event_name, **kwargs):
    print(f"Event: {event_name}")
```

**Class Handlers:**
```python
class MyHandler(EventHandler):
    def event_name(self, param1, param2):
        service = self.get_di().get('service')
```

### Priorities

- Lower numbers execute first (1 before 100)
- Default priority is 100
- Group related priorities (1-10 auth, 50-60 logic, 100+ logging)

## Common Patterns

### Event-Driven Architecture
Use events to decouple components and create flexible, maintainable applications.

### Plugin Systems
Register plugins as event handlers for extensibility.

### Pipeline Processing
Use priorities to create processing pipelines (validation, processing, logging).

### Audit Trail
Register audit handlers at low priority to log all events.

## See Also

- [Event System Documentation](../../docs/event/index.md)
- [Dependency Injection Examples](../base/)
- [Form Examples](../form/)
