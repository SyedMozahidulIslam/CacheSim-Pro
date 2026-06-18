"""
algorithm_factory.py
────────────────────
Factory Pattern: creates cache algorithm objects by name.

To add a NEW algorithm (e.g. LFU):
    1. Create core/lfu_cache.py  inheriting CacheBase
    2. Import it here
    3. Add one line to ALGORITHM_MAP
    That's it — zero changes needed anywhere else.
"""

from core.fifo_cache import FIFOCache
from core.lru_cache import LRUCache

# ─── Registry: maps algorithm name → class ───────────────────────────────────
# Add future algorithms here with one line
ALGORITHM_MAP = {
    "FIFO": FIFOCache,
    "LRU" : LRUCache,
}


class AlgorithmFactory:
    """Creates cache algorithm instances by name string."""

    @staticmethod
    def create(algo_name: str, capacity: int):
        """
        Instantiate a cache algorithm by name.

        Args:
            algo_name (str): Algorithm name — "FIFO" or "LRU"
            capacity  (int): Cache size (number of slots)

        Returns:
            CacheBase subclass instance

        Raises:
            ValueError: If algo_name is not in the registry
        """
        algo_class = ALGORITHM_MAP.get(algo_name.upper())

        if algo_class is None:
            available = ", ".join(ALGORITHM_MAP.keys())
            raise ValueError(
                f"Unknown algorithm '{algo_name}'. "
                f"Available options: {available}"
            )

        return algo_class(capacity)

    @staticmethod
    def available_algorithms() -> list:
        """Returns list of registered algorithm names for GUI dropdown."""
        return list(ALGORITHM_MAP.keys())
