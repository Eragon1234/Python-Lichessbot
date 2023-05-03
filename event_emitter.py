from typing import Any, Callable


class EventEmitter:

    def __init__(self):
        self.handlers = {}

    def on(self, event: str, handler: Callable[..., None]):
        if event not in self.handlers:
            self.handlers[event] = []

        self.handlers[event].append(handler)

    def emit(self, event: str, *args):
        for handler in self.handlers[event]:
            handler(*args)
