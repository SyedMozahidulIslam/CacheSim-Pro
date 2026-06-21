"""
simulator.py
────────────
The simulation engine — orchestrates one step at a time.

StepResult is the data packet passed from engine → GUI.
Simulator drives the algorithm and stats on each step.
"""

from dataclasses import dataclass, field
from core.algorithm_factory import AlgorithmFactory
from engine.stats_manager import StatsManager


@dataclass
class StepResult:
    """
    Data packet produced after each simulation step.
    Passed directly to the GUI for display — no GUI logic here.
    """
    page        : int             # Page number that was requested
    is_hit      : bool            # True = hit, False = miss
    cache_state : list            # Snapshot of cache after this access
    replaced    : object          # Evicted page number, or None
    stats       : dict            # Current hit/miss statistics
    step_index  : int             # Which step we're on (0-based)
    total_steps : int             # Total references in the string


class Simulator:
    """
    Drives the cache simulation step-by-step.

    Usage:
        sim = Simulator("LRU", 3, [1, 2, 3, 2, 4])
        while not sim.is_done():
            result = sim.step()
            # pass result to GUI
    """

    def __init__(self, algo_name: str, capacity: int, reference_string: list):
        """
        Args:
            algo_name        (str):  "FIFO" or "LRU"
            capacity         (int):  Number of cache slots
            reference_string (list): List of page integers to process
        """
        self.reference_string = reference_string
        self.total_steps      = len(reference_string)
        self.current_index    = 0

        # Create algorithm via factory (Strategy Pattern)
        self.algorithm = AlgorithmFactory.create(algo_name, capacity)
        self.stats     = StatsManager()

    def step(self) -> StepResult:
        """
        Process the next page reference.

        Returns:
            StepResult: complete snapshot of this step's outcome

        Raises:
            IndexError: if called after simulation is already done
        """
        if self.is_done():
            raise IndexError("Simulation is already complete.")

        # Get the next page from the reference string
        page = self.reference_string[self.current_index]

        # Run the algorithm — get hit/miss and evicted page
        is_hit, replaced = self.algorithm.access(page)

        # Record in stats
        self.stats.record(is_hit)

        # Build the result packet
        result = StepResult(
            page        = page,
            is_hit      = is_hit,
            cache_state = self.algorithm.get_state(),
            replaced    = replaced,
            stats       = self.stats.get_stats(),
            step_index  = self.current_index,
            total_steps = self.total_steps,
        )

        self.current_index += 1
        return result

    def reset(self):
        """Resets simulation to the beginning."""
        self.current_index = 0
        self.algorithm.reset()
        self.stats.reset()

    def is_done(self) -> bool:
        """Returns True when all references have been processed."""
        return self.current_index >= self.total_steps
