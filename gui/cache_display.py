"""
cache_display.py
────────────────
The visual heart of CacheSim Pro.
Draws colored cache blocks on a canvas and shows step information.

Color scheme:
    GREEN  (#2ECC71) = Cache Hit
    RED    (#E74C3C) = Cache Miss (newly loaded page)
    YELLOW (#F39C12) = Replaced / evicted block
    GRAY   (#4A4A6A) = Empty slot
"""

import tkinter as tk


class CacheDisplay(tk.Frame):
    """Animated cache block visualization panel."""

    # ── Colors ────────────────────────────────────────────────────────────────
    BG           = "#1E1E2E"
    EMPTY_COLOR  = "#4A4A6A"
    HIT_COLOR    = "#2ECC71"
    MISS_COLOR   = "#E74C3C"
    REPLACE_COLOR= "#F39C12"
    TEXT_LIGHT   = "#FFFFFF"
    TEXT_DARK    = "#1E1E2E"
    LABEL_FG     = "#A0A0B0"
    ACCENT_FG    = "#7C83FD"

    # ── Block dimensions ─────────────────────────────────────────────────────
    BLOCK_W      = 90
    BLOCK_H      = 70
    BLOCK_GAP    = 16
    CANVAS_H     = 200

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=self.BG, **kwargs)
        self._capacity    = 0
        self._last_result = None
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        """Build the canvas and info labels."""
        # ── Step info bar ─────────────────────────────────────────────────
        info_frame = tk.Frame(self, bg=self.BG)
        info_frame.pack(fill="x", padx=16, pady=(12, 4))

        self.step_label = tk.Label(
            info_frame, text="Configure and press  ▶ Start",
            bg=self.BG, fg=self.ACCENT_FG,
            font=("Consolas", 13, "bold")
        )
        self.step_label.pack(side="left")

        self.decision_label = tk.Label(
            info_frame, text="",
            bg=self.BG, fg=self.LABEL_FG,
            font=("Consolas", 11)
        )
        self.decision_label.pack(side="right")

        # ── Canvas for cache blocks ───────────────────────────────────────
        self.canvas = tk.Canvas(
            self, bg=self.BG, height=self.CANVAS_H,
            highlightthickness=0
        )
        self.canvas.pack(fill="x", padx=16, pady=8)

        # ── Reference string progress bar ────────────────────────────────
        self.progress_label = tk.Label(
            self, text="",
            bg=self.BG, fg=self.LABEL_FG,
            font=("Consolas", 10), wraplength=700, justify="left"
        )
        self.progress_label.pack(anchor="w", padx=16, pady=(0, 8))

        # ── Legend ───────────────────────────────────────────────────────
        self._build_legend()

    def _build_legend(self):
        """Draw the color legend below the canvas."""
        leg = tk.Frame(self, bg=self.BG)
        leg.pack(pady=(0, 8))

        items = [
            (self.HIT_COLOR,    "Cache Hit"),
            (self.MISS_COLOR,   "Cache Miss"),
            (self.REPLACE_COLOR,"Replaced"),
            (self.EMPTY_COLOR,  "Empty Slot"),
        ]
        for color, label in items:
            dot = tk.Label(leg, text="●", bg=self.BG, fg=color,
                           font=("Consolas", 14))
            dot.pack(side="left", padx=(12, 2))
            tk.Label(leg, text=label, bg=self.BG, fg=self.LABEL_FG,
                     font=("Consolas", 9)).pack(side="left", padx=(0, 8))

    # ─────────────────────────────────────────────────────────────────────────
    def set_capacity(self, capacity: int):
        """Call this when simulation starts to set number of slots."""
        self._capacity = capacity
        self._draw_empty_blocks()

    def _draw_empty_blocks(self):
        """Draw all cache slots as empty (gray)."""
        self.canvas.delete("all")
        total_w = self._capacity * (self.BLOCK_W + self.BLOCK_GAP) - self.BLOCK_GAP
        start_x = max(16, (self.canvas.winfo_width() - total_w) // 2)
        if start_x < 16:
            start_x = 16

        cy = self.CANVAS_H // 2

        for i in range(self._capacity):
            x = start_x + i * (self.BLOCK_W + self.BLOCK_GAP)
            self._draw_block(x, cy - self.BLOCK_H // 2,
                             self.EMPTY_COLOR, "—", f"Slot {i}")

    def _draw_block(self, x: int, y: int, color: str,
                    value: str, sublabel: str):
        """Draw a single cache block rectangle with value and label."""
        r = 8   # corner radius
        x2, y2 = x + self.BLOCK_W, y + self.BLOCK_H

        # Rounded rectangle via polygon approximation
        self.canvas.create_polygon(
            x+r, y,  x2-r, y,  x2, y+r,
            x2, y2-r, x2-r, y2, x+r, y2,
            x, y2-r, x, y+r,
            fill=color, outline="", smooth=True
        )

        # Page number (large center text)
        text_color = self.TEXT_DARK if color in (
            self.HIT_COLOR, self.REPLACE_COLOR) else self.TEXT_LIGHT

        self.canvas.create_text(
            x + self.BLOCK_W // 2, y + self.BLOCK_H // 2 - 8,
            text=str(value), fill=text_color,
            font=("Consolas", 20, "bold")
        )

        # Slot label (small bottom text)
        self.canvas.create_text(
            x + self.BLOCK_W // 2, y + self.BLOCK_H - 12,
            text=sublabel, fill=text_color,
            font=("Consolas", 8)
        )

    # ─────────────────────────────────────────────────────────────────────────
    def update(self, result, reference_string: list = None):
        """
        Redraw cache blocks based on the latest StepResult.

        Args:
            result           : StepResult from simulator
            reference_string : Full list for progress display
        """
        self._last_result = result
        self.canvas.delete("all")

        cache_state = result.cache_state
        capacity    = self._capacity

        # Calculate layout
        total_w  = capacity * (self.BLOCK_W + self.BLOCK_GAP) - self.BLOCK_GAP
        cw       = self.canvas.winfo_width()
        start_x  = max(16, (cw - total_w) // 2) if cw > 100 else 30
        cy       = self.CANVAS_H // 2

        for i in range(capacity):
            x     = start_x + i * (self.BLOCK_W + self.BLOCK_GAP)
            y     = cy - self.BLOCK_H // 2

            if i < len(cache_state):
                page = cache_state[i]

                # Determine block color
                if page == result.page and result.is_hit:
                    color = self.HIT_COLOR          # GREEN  — hit
                elif page == result.replaced:
                    color = self.REPLACE_COLOR      # YELLOW — replaced
                elif page == result.page and not result.is_hit:
                    color = self.MISS_COLOR         # RED    — newly loaded
                else:
                    color = self.EMPTY_COLOR        # GRAY   — unchanged

                self._draw_block(x, y, color, page, f"Slot {i}")
            else:
                # Empty slot
                self._draw_block(x, y, self.EMPTY_COLOR, "—", f"Slot {i}")

        # ── Update step info labels ───────────────────────────────────────
        step_text = (
            f"Step {result.step_index + 1} / {result.total_steps}"
            f"   →   Page Requested: {result.page}"
        )
        self.step_label.config(text=step_text)

        if result.is_hit:
            decision = f"✅  HIT  — Page {result.page} already in cache"
            self.decision_label.config(text=decision, fg=self.HIT_COLOR)
        else:
            if result.replaced is not None:
                decision = (f"❌  MISS  — Page {result.replaced} "
                            f"replaced by Page {result.page}")
            else:
                decision = f"❌  MISS  — Page {result.page} loaded into empty slot"
            self.decision_label.config(text=decision, fg=self.MISS_COLOR)

        # ── Progress indicator ────────────────────────────────────────────
        if reference_string:
            self._update_progress(reference_string, result.step_index)

    def _update_progress(self, ref_string: list, current_idx: int):
        """Show the reference string with current position highlighted."""
        parts = []
        for i, page in enumerate(ref_string):
            if i < current_idx:
                parts.append(f" {page} ")
            elif i == current_idx:
                parts.append(f"[{page}]")
            else:
                parts.append(f" {page} ")
        self.progress_label.config(
            text="Reference String:  " + " ".join(parts)
        )

    def reset(self):
        """Clear display back to initial state."""
        self.canvas.delete("all")
        self.step_label.config(
            text="Configure and press  ▶ Start",
            fg=self.ACCENT_FG
        )
        self.decision_label.config(text="")
        self.progress_label.config(text="")
        self._capacity    = 0
        self._last_result = None
