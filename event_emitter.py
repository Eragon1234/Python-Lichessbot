from typing import Any, Callable


class EventEmitter:
    handlers = {}

    def on(self, event: str, handler: Callable[[*Any], None]):
        if event not in self.handlers:
            self.handlers[event] = []

        self.handlers[event].append(handler)

    def emit(self, event: str, *args):
        for handler in self.handlers[event]:
            handler(*args)
