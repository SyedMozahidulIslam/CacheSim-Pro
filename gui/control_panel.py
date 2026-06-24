"""
control_panel.py
────────────────
Top panel with all user inputs and simulation control buttons.
Communicates upward to MainWindow via callback functions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core.algorithm_factory import AlgorithmFactory
from utils.validators import validate_cache_size, validate_reference_string


class ControlPanel(tk.Frame):
    """Input fields and simulation control buttons."""

    # ── Colors ────────────────────────────────────────────────────────────────
    BG       = "#12121E"
    FIELD_BG = "#2A2A3E"
    FIELD_FG = "#FFFFFF"
    LABEL_FG = "#A0A0B0"
    ACCENT   = "#7C83FD"

    BTN_START  = {"bg": "#2ECC71", "fg": "#000000", "text": "▶  Start"}
    BTN_NEXT   = {"bg": "#3498DB", "fg": "#FFFFFF",  "text": "⏭  Next Step"}
    BTN_AUTO   = {"bg": "#F39C12", "fg": "#000000",  "text": "⚡  Auto Play"}
    BTN_RESET  = {"bg": "#E74C3C", "fg": "#FFFFFF",  "text": "↺  Reset"}

    DEFAULT_REF  = "1 2 3 2 4 1 5 2 3"
    DEFAULT_SIZE = "3"
    AUTO_DELAY_MS = 800          # milliseconds between auto-play steps

    def __init__(self, parent, callbacks: dict, **kwargs):
        """
        Args:
            parent    : Parent widget
            callbacks : dict with keys 'start', 'next', 'auto', 'reset'
                        pointing to MainWindow handler methods
        """
        super().__init__(parent, bg=self.BG, **kwargs)
        self._callbacks    = callbacks
        self._auto_running = False
        self._auto_job     = None
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        """Assemble header, input row, and button row."""
        self._build_header()
        self._build_inputs()
        self._build_buttons()

    def _build_header(self):
        """App title bar."""
        hdr = tk.Frame(self, bg=self.ACCENT, height=4)
        hdr.pack(fill="x")

        title_frame = tk.Frame(self, bg=self.BG)
        title_frame.pack(fill="x", padx=16, pady=(10, 4))

        tk.Label(
            title_frame, text="⚙  CacheSim Pro",
            bg=self.BG, fg=self.ACCENT,
            font=("Consolas", 16, "bold")
        ).pack(side="left")

        tk.Label(
            title_frame,
            text="Cache Memory Simulator  |  Educational Tool",
            bg=self.BG, fg=self.LABEL_FG,
            font=("Consolas", 9)
        ).pack(side="right", pady=6)

    def _build_inputs(self):
        """Algorithm dropdown, cache size field, reference string field."""
        row = tk.Frame(self, bg=self.BG)
        row.pack(fill="x", padx=16, pady=8)

        # ── Algorithm selector ────────────────────────────────────────────
        self._make_label(row, "Algorithm")
        self.algo_var = tk.StringVar(value="FIFO")
        algo_cb = ttk.Combobox(
            row, textvariable=self.algo_var,
            values=AlgorithmFactory.available_algorithms(),
            state="readonly", width=8,
            font=("Consolas", 11)
        )
        algo_cb.pack(side="left", padx=(0, 24))

        # ── Cache size ────────────────────────────────────────────────────
        self._make_label(row, "Cache Size")
        self.size_entry = tk.Entry(
            row, width=5,
            bg=self.FIELD_BG, fg=self.FIELD_FG,
            insertbackground=self.FIELD_FG,
            font=("Consolas", 12), relief="flat",
            highlightthickness=1, highlightcolor=self.ACCENT,
            highlightbackground=self.FIELD_BG
        )
        self.size_entry.insert(0, self.DEFAULT_SIZE)
        self.size_entry.pack(side="left", padx=(0, 24), ipady=4)

        # ── Reference string ──────────────────────────────────────────────
        self._make_label(row, "Reference String")
        self.ref_entry = tk.Entry(
            row, width=36,
            bg=self.FIELD_BG, fg=self.FIELD_FG,
            insertbackground=self.FIELD_FG,
            font=("Consolas", 12), relief="flat",
            highlightthickness=1, highlightcolor=self.ACCENT,
            highlightbackground=self.FIELD_BG
        )
        self.ref_entry.insert(0, self.DEFAULT_REF)
        self.ref_entry.pack(side="left", ipady=4)

    def _make_label(self, parent, text: str):
        """Helper to create a consistent input label."""
        tk.Label(
            parent, text=text,
            bg=self.BG, fg=self.LABEL_FG,
            font=("Consolas", 9)
        ).pack(side="left", padx=(0, 6))

    def _build_buttons(self):
        """Start, Next Step, Auto Play, Reset buttons."""
        row = tk.Frame(self, bg=self.BG)
        row.pack(fill="x", padx=16, pady=(0, 12))

        btn_defs = [
            (self.BTN_START, self._on_start),
            (self.BTN_NEXT,  self._on_next),
            (self.BTN_AUTO,  self._on_auto),
            (self.BTN_RESET, self._on_reset),
        ]

        self._buttons = {}
        for spec, cmd in btn_defs:
            btn = tk.Button(
                row, text=spec["text"],
                bg=spec["bg"], fg=spec["fg"],
                font=("Consolas", 10, "bold"),
                relief="flat", cursor="hand2",
                padx=16, pady=6,
                activebackground=spec["bg"],
                activeforeground=spec["fg"],
                command=cmd
            )
            btn.pack(side="left", padx=(0, 10))
            self._buttons[spec["text"]] = btn

        # Status message label (right side)
        self.status_label = tk.Label(
            row, text="",
            bg=self.BG, fg=self.LABEL_FG,
            font=("Consolas", 9)
        )
        self.status_label.pack(side="right")

    # ─────────────────────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────────────────────
    def get_config(self) -> dict:
        """
        Validate and return current input values.

        Returns:
            dict: {algo, cache_size, reference_string}

        Raises:
            ValueError: Propagated from validators
        """
        algo       = self.algo_var.get()
        cache_size = validate_cache_size(self.size_entry.get())
        ref_string = validate_reference_string(self.ref_entry.get())
        return {"algo": algo, "cache_size": cache_size,
                "reference_string": ref_string}

    def set_status(self, msg: str, color: str = "#A0A0B0"):
        """Display a status message in the control bar."""
        self.status_label.config(text=msg, fg=color)

    def set_simulation_active(self, active: bool):
        """Disable inputs while simulation is running."""
        state = "disabled" if active else "normal"
        self.size_entry.config(state=state)
        self.ref_entry.config(state=state)

    def stop_autoplay(self):
        """Externally stop autoplay (e.g. when simulation ends)."""
        self._auto_running = False
        if self._auto_job:
            self.after_cancel(self._auto_job)
            self._auto_job = None
        # Reset auto button text
        for key, btn in self._buttons.items():
            if "Auto" in key:
                btn.config(text=self.BTN_AUTO["text"])

    # ─────────────────────────────────────────────────────────────────────────
    # Button handlers
    # ─────────────────────────────────────────────────────────────────────────
    def _on_start(self):
        try:
            config = self.get_config()
            self._callbacks["start"](config)
            self.set_simulation_active(True)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _on_next(self):
        self._callbacks["next"]()

    def _on_auto(self):
        if self._auto_running:
            # Pause autoplay
            self.stop_autoplay()
            for key, btn in self._buttons.items():
                if "Auto" in key:
                    btn.config(text=self.BTN_AUTO["text"])
        else:
            # Start autoplay
            self._auto_running = True
            for key, btn in self._buttons.items():
                if "Auto" in key:
                    btn.config(text="⏸  Pause")
            self._run_auto_step()

    def _run_auto_step(self):
        """Recursively schedules next step until done or paused."""
        if not self._auto_running:
            return
        done = self._callbacks["auto_step"]()
        if not done:
            self._auto_job = self.after(self.AUTO_DELAY_MS, self._run_auto_step)
        else:
            self.stop_autoplay()

    def _on_reset(self):
        self.stop_autoplay()
        self.set_simulation_active(False)
        self._callbacks["reset"]()
