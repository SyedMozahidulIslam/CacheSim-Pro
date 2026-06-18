"""
lru_cache.py
────────────
LRU (Least Recently Used) Cache Replacement Algorithm.

Teaching Concept:
    Track WHEN each page was last used.
    The page sitting idle the LONGEST gets evicted.
    Recently used pages are "hot" — they stay.

Visual Example (cache size = 3):
    Reference: 1 2 3 2 4
    After 1:   [1]          Miss
    After 2:   [1,2]        Miss
    After 3:   [1,2,3]      Miss — full, order: 1(LRU)→2→3(MRU)
    After 2:   [1,3,2]      HIT  — 2 refreshed, order: 1(LRU)→3→2(MRU)
    After 4:   [3,2,4]      Miss — 1 evicted (LRU), order: 3→2→4

Key Insight — OrderedDict trick:
    • Items at FRONT  = Least Recently Used  → evict first
    • Items at END    = Most Recently Used   → keep longest
    • On HIT: move_to_end()   (refresh to MRU position)
    • On MISS: popitem(last=False) (evict LRU from front)

Time Complexity: O(1) for both access and eviction
"""

from collections import OrderedDict
from core.cache_base import CacheBase


class LRUCache(CacheBase):
    """LRU cache: evicts the page least recently accessed."""

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._order = OrderedDict()   # page → None  (value unused)

    def access(self, page: int) -> tuple:
        """
        Process one page reference with LRU replacement.

        Cases:
            1. HIT      → move page to MRU end, nothing evicted
            2. MISS + space → insert at MRU end, no eviction
            3. MISS + full  → evict LRU front, insert at MRU end

        Args:
            page (int): Page number being requested

        Returns:
            (is_hit: bool, replaced: int | None)
        """
        # ── Case 1: Cache Hit ─────────────────────────────────────────────
        if page in self._order:
            # Refresh recency — move to most-recently-used end
            self._order.move_to_end(page)
            self.cache = list(self._order.keys())
            return (True, None)

        replaced = None

        # ── Case 2 & 3: Cache Miss ────────────────────────────────────────
        if len(self._order) >= self.capacity:
            # Evict least recently used (front of OrderedDict)
            replaced, _ = self._order.popitem(last=False)

        # Insert new page at MRU end
        self._order[page] = None
        self.cache = list(self._order.keys())

        return (False, replaced)

    def get_state(self) -> list:
        """Returns pages from LRU (oldest) → MRU (newest)."""
        return list(self._order.keys())

    def reset(self):
        """Clear all state."""
        super().reset()
        self._order.clear()
