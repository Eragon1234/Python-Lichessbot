from typing import TypeVar, Generic, Hashable, Optional

from cache.lru.node import LRUNode

K = TypeVar("K", bound=Hashable)
T = TypeVar("T")

DUMMY_VALUE = object()


class LRUCache(Generic[K, T]):
    def __init__(self, size: int):
        self.size = size

        self.map = {}
        self.newest = LRUNode(DUMMY_VALUE, None)
        self.oldest = LRUNode(DUMMY_VALUE, None)
        self.newest.right = self.oldest
        self.oldest.left = self.newest

    def get(self, key: K) -> Optional[T]:
        if key not in self.map:
            return None

        node = self.map[key]

        self.remove(key)
        self._insert(node.key, node.value)

        return node.value

    def set(self, key: K, value: T):
        if key in self.map:
            self.remove(key)

        self._insert(key, value)

        if len(self.map) > self.size:
            self.remove_oldest()

    def _insert(self, key: K, value: T):
        node = LRUNode(key, value)
        self.map[key] = node

        node.left = self.newest
        node.right = self.newest.right
        self.newest.right = node
        node.right.left = node

    def remove(self, key: K):
        if key not in self.map:
            return

        node = self.map[key]
        node.left.right = node.right
        node.right.left = node.left
        del self.map[key]

    def remove_oldest(self):
        self.remove(self.oldest.left.key)
