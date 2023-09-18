from dataclasses import dataclass
from typing import TypeVar, Generic, Hashable

T = TypeVar("T")


@dataclass
class LRUNode(Generic[T]):
    value: T
    key: Hashable
    left: "LRUNode" = None
    right: "LRUNode" = None
