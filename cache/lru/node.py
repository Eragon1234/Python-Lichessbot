from typing import TypeVar, Generic, Hashable

T = TypeVar("T")


class LRUNode(Generic[T]):
    def __init__(self, key: Hashable, value, left: "LRUNode" = None, right: "LRUNode" = None):
        self.value = value
        self.key = key

        self.left = left
        self.right = right
