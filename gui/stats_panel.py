"""
stats_panel.py
──────────────
Displays live simulation statistics at the bottom of the window.
Updates after every simulation step.
"""

import tkinter as tk


class StatsPanel(tk.Frame):
    """Live statistics display panel."""

    # ── Color constants ───────────────────────────────────────────────────────
    BG          = "#1E1E2E"
    CARD_BG     = "#2A2A3E"
    HIT_COLOR   = "#2ECC71"
    MISS_COLOR  = "#E74C3C"
    TOTAL_COLOR = "#3498DB"
    RATIO_COLOR = "#F39C12"
    LABEL_FG    = "#A0A0B0"
    VALUE_FG    = "#FFFFFF"

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=self.BG, **kwargs)
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        """Create all stat cards in a single row."""
        title = tk.Label(
            self, text="📊  STATISTICS",
            bg=self.BG, fg=self.LABEL_FG,
            font=("Consolas", 10, "bold"), pady=6
        )
        title.pack(anchor="w", padx=16)

        cards_frame = tk.Frame(self, bg=self.BG)
        cards_frame.pack(fill="x", padx=12, pady=(0, 10))

        # Define stat cards: (label, initial_value, accent_color, attr_name)
        card_defs = [
            ("TOTAL REQUESTS", "0",      self.TOTAL_COLOR, "total_var"),
            ("CACHE HITS",     "0",      self.HIT_COLOR,   "hits_var"),
            ("CACHE MISSES",   "0",      self.MISS_COLOR,  "misses_var"),
            ("HIT RATIO",      "0.00%",  self.RATIO_COLOR, "hit_ratio_var"),
            ("MISS RATIO",     "0.00%",  self.RATIO_COLOR, "miss_ratio_var"),
        ]

        for i, (label, init_val, color, attr) in enumerate(card_defs):
            var = tk.StringVar(value=init_val)
            setattr(self, attr, var)
            self._make_card(cards_frame, label, var, color, i)

    def _make_card(self, parent, label: str, var: tk.StringVar,
                   accent: str, col: int):
        """Build a single statistics card widget."""
        card = tk.Frame(parent, bg=self.CARD_BG, bd=0, relief="flat")
        card.grid(row=0, column=col, padx=5, pady=4, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        # Accent bar at top of card
        bar = tk.Frame(card, bg=accent, height=3)
        bar.pack(fill="x")

        # Stat value (large)
        tk.Label(
            card, textvariable=var,
            bg=self.CARD_BG, fg=accent,
            font=("Consolas", 18, "bold"), pady=4
        ).pack()

        # Stat label (small)
        tk.Label(
            card, text=label,
            bg=self.CARD_BG, fg=self.LABEL_FG,
            font=("Consolas", 8), pady=2
        ).pack()

    # ─────────────────────────────────────────────────────────────────────────
    def update(self, stats: dict):
        """
        Refresh all stat values from a stats dictionary.

        Args:
            stats (dict): From StatsManager.get_stats()
        """
        self.total_var.set(str(stats["total"]))
        self.hits_var.set(str(stats["hits"]))
        self.misses_var.set(str(stats["misses"]))
        self.hit_ratio_var.set(f'{stats["hit_ratio"]:.2f}%')
        self.miss_ratio_var.set(f'{stats["miss_ratio"]:.2f}%')

    def reset(self):
        """Reset all stats to zero."""
        self.total_var.set("0")
        self.hits_var.set("0")
        self.misses_var.set("0")
        self.hit_ratio_var.set("0.00%")
        self.miss_ratio_var.set("0.00%")
