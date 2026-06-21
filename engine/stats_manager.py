"""
stats_manager.py
────────────────
Single Responsibility: track and compute simulation statistics.
Completely decoupled from GUI and algorithm logic.
"""


class StatsManager:
    """Tracks hits, misses, and computes ratios for the simulation."""

    def __init__(self):
        self.reset()

    def record(self, is_hit: bool):
        """
        Record the result of a single cache access.

        Args:
            is_hit (bool): True for cache hit, False for cache miss
        """
        self.total += 1
        if is_hit:
            self.hits += 1
        else:
            self.misses += 1

    def get_stats(self) -> dict:
        """
        Returns all statistics as a dictionary.

        Returns:
            dict with keys: total, hits, misses, hit_ratio, miss_ratio
        """
        hit_ratio  = (self.hits   / self.total * 100) if self.total > 0 else 0.0
        miss_ratio = (self.misses / self.total * 100) if self.total > 0 else 0.0

        return {
            "total"     : self.total,
            "hits"      : self.hits,
            "misses"    : self.misses,
            "hit_ratio" : round(hit_ratio,  2),
            "miss_ratio": round(miss_ratio, 2),
        }

    def reset(self):
        """Reset all counters to zero."""
        self.total  = 0
        self.hits   = 0
        self.misses = 0
