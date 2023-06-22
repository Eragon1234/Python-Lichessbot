from typing import Callable


class EventEmitter:
    """A simple event emitter."""

    def __init__(self):
        self.handlers = {}

    def on(self, event: str, handler: Callable[..., None]):
        """Registers a handler for an event."""
        if event not in self.handlers:
            self.handlers[event] = []

        self.handlers[event].append(handler)

    def emit(self, event: str, *args):
        """Emits an event."""
        for handler in self.handlers[event]:
            handler(*args)
