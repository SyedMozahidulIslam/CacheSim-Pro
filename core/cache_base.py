"""
cache_base.py
─────────────
Abstract base class that defines the contract every cache algorithm must follow.
Uses the Strategy Pattern — swap algorithms without touching any other code.
"""

from abc import ABC, abstractmethod


class CacheBase(ABC):
    """
    Abstract base for all cache replacement algorithms.
    Every algorithm (FIFO, LRU, LFU, etc.) must inherit this class
    and implement the access() method.
    """

    def __init__(self, capacity: int):
        """
        Args:
            capacity (int): Maximum number of pages the cache can hold.
        """
        self.capacity = capacity
        self.cache = []          # Holds current pages in cache

    @abstractmethod
    def access(self, page: int) -> tuple:
        """
        Process a single page reference.

        Args:
            page (int): The page number being requested.

        Returns:
            tuple: (is_hit: bool, replaced_page: int | None)
                   is_hit      → True if page was already in cache
                   replaced    → Page that was evicted, or None
        """
        pass

    def get_state(self) -> list:
        """Returns a snapshot of current cache contents."""
        return list(self.cache)

    def reset(self):
        """Clears cache back to empty state."""
        self.cache = []
