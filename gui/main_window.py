"""
main_window.py
──────────────
Root application window. Assembles all panels and owns the Simulator.
Acts as the Controller in MVC — receives GUI events, drives simulation,
and pushes results back to the display panels.
"""

import tkinter as tk
from tkinter import messagebox

from engine.simulator import Simulator
from gui.control_panel import ControlPanel
from gui.cache_display import CacheDisplay
from gui.stats_panel import StatsPanel


class MainWindow:
    """
    Root Tkinter window for CacheSim Pro.
    Owns the Simulator and coordinates all GUI panels.
    """

    BG     = "#1E1E2E"
    WIDTH  = 860
    HEIGHT = 680

    def __init__(self):
        self.root      = tk.Tk()
        self.simulator = None
        self._ref_string = []

        self._configure_root()
        self._build_panels()

    # ─────────────────────────────────────────────────────────────────────────
    def _configure_root(self):
        """Set window properties."""
        self.root.title("CacheSim Pro — Cache Memory Simulator")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.minsize(720, 580)
        self.root.configure(bg=self.BG)
        self.root.resizable(True, True)

        # Center on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - self.WIDTH)  // 2
        y = (self.root.winfo_screenheight() - self.HEIGHT) // 2
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def _build_panels(self):
        """Assemble ControlPanel → CacheDisplay → StatsPanel top-to-bottom."""

        # ── Control Panel (top) ───────────────────────────────────────────
        self.control = ControlPanel(
            self.root,
            callbacks={
                "start"    : self._on_start,
                "next"     : self._on_next,
                "auto_step": self._on_auto_step,
                "reset"    : self._on_reset,
            }
        )
        self.control.pack(fill="x")

        # Divider
        tk.Frame(self.root, bg="#2A2A3E", height=2).pack(fill="x")

        # ── Cache Display (middle — takes most space) ─────────────────────
        self.cache_display = CacheDisplay(self.root)
        self.cache_display.pack(fill="both", expand=True)

        # Divider
        tk.Frame(self.root, bg="#2A2A3E", height=2).pack(fill="x")

        # ── Stats Panel (bottom) ──────────────────────────────────────────
        self.stats_panel = StatsPanel(self.root)
        self.stats_panel.pack(fill="x")

    # ─────────────────────────────────────────────────────────────────────────
    # Simulation Callbacks
    # ─────────────────────────────────────────────────────────────────────────
    def _on_start(self, config: dict):
        """
        Called when user clicks Start.
        Builds a fresh Simulator from the config dict.
        """
        self._ref_string = config["reference_string"]

        # Build simulator
        self.simulator = Simulator(
            algo_name        = config["algo"],
            capacity         = config["cache_size"],
            reference_string = self._ref_string,
        )

        # Prepare display
        self.cache_display.set_capacity(config["cache_size"])
        self.stats_panel.reset()

        # Update root title to show current config
        self.root.title(
            f"CacheSim Pro  |  {config['algo']}  |  "
            f"Cache Size: {config['cache_size']}"
        )

        self.control.set_status(
            f"▶  Simulation ready — {len(self._ref_string)} references  |  "
            f"Press 'Next Step' or 'Auto Play'",
            color="#7C83FD"
        )

    def _on_next(self):
        """Process exactly one step."""
        if not self._check_simulator_ready():
            return
        self._do_step()

    def _on_auto_step(self) -> bool:
        """
        Called repeatedly by ControlPanel's auto-play timer.
        Returns True when simulation is complete (signals stop).
        """
        if not self._check_simulator_ready(silent=True):
            return True
        self._do_step()
        return self.simulator.is_done()

    def _on_reset(self):
        """Reset everything to blank state."""
        self.simulator = None
        self._ref_string = []
        self.cache_display.reset()
        self.stats_panel.reset()
        self.control.set_status("")
        self.root.title("CacheSim Pro — Cache Memory Simulator")

    # ─────────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────────────────────
    def _do_step(self):
        """Execute one simulation step and push result to GUI panels."""
        if self.simulator.is_done():
            self._on_simulation_complete()
            return

        result = self.simulator.step()

        # Push to both display panels
        self.cache_display.update(result, self._ref_string)
        self.stats_panel.update(result.stats)

        # Status bar feedback
        status = (
            f"Step {result.step_index + 1}/{result.total_steps}  "
            f"→  {'HIT ✅' if result.is_hit else 'MISS ❌'}"
        )
        color = "#2ECC71" if result.is_hit else "#E74C3C"
        self.control.set_status(status, color)

        if self.simulator.is_done():
            self._on_simulation_complete()

    def _on_simulation_complete(self):
        """Called when last reference has been processed."""
        self.control.stop_autoplay()
        stats = self.simulator.stats.get_stats()
        self.control.set_status(
            f"✅  Simulation complete  |  "
            f"Hit Rate: {stats['hit_ratio']:.2f}%  |  "
            f"Miss Rate: {stats['miss_ratio']:.2f}%",
            color="#2ECC71"
        )

    def _check_simulator_ready(self, silent: bool = False) -> bool:
        """Guard: make sure simulator exists before stepping."""
        if self.simulator is None:
            if not silent:
                messagebox.showwarning(
                    "Not Started",
                    "Please configure and press ▶ Start first."
                )
            return False
        return True

    # ─────────────────────────────────────────────────────────────────────────
    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()
