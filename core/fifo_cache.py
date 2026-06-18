"""
fifo_cache.py
─────────────
FIFO (First-In First-Out) Cache Replacement Algorithm.

Teaching Concept:
    Imagine a queue at a checkout line.
    The person who joined FIRST leaves FIRST.
    The OLDEST page in cache gets evicted when cache is full.

Visual Example (cache size = 3):
    Reference: 1 2 3 4
    After 1: [1]         Miss — loaded
    After 2: [1,2]       Miss — loaded
    After 3: [1,2,3]     Miss — loaded (cache full)
    After 4: [2,3,4]     Miss — 1 evicted (it was FIRST in)

Data Structure: collections.deque
    deque.append()     → add to right  (newest)
    deque.popleft()    → remove left   (oldest = FIFO victim)
    O(1) for both ends
"""

from collections import deque
from core.cache_base import CacheBase


class FIFOCache(CacheBase):
    """FIFO cache: evicts the page that arrived earliest."""

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._queue = deque()

    def access(self, page: int) -> tuple:
        """
        Process one page reference with FIFO replacement.

        Cases:
            1. HIT      → page in cache, nothing changes
            2. MISS + space → load page, no eviction
            3. MISS + full  → evict oldest, load new page

        Args:
            page (int): Page number being requested

        Returns:
            (is_hit: bool, replaced: int | None)
        """
        # ── Case 1: Cache Hit ─────────────────────────────────────────────
        if page in self._queue:
            self.cache = list(self._queue)
            return (True, None)

        replaced = None

        # ── Case 2 & 3: Cache Miss ────────────────────────────────────────
        if len(self._queue) >= self.capacity:
            # Cache full → evict the oldest (leftmost) page
            replaced = self._queue.popleft()

        # Load new page at the back (most recently arrived)
        self._queue.append(page)
        self.cache = list(self._queue)

        return (False, replaced)

    def get_state(self) -> list:
        """Returns pages in insertion order: oldest → newest."""
        return list(self._queue)

    def reset(self):
        """Clear all state."""
        super().reset()
        self._queue.clear()
