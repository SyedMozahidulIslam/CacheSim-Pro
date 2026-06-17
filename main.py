"""
main.py
───────
CacheSim Pro — Cache Memory Simulator
Entry point. Run this file to launch the application.

Usage:
    python main.py
"""

import sys
import os

# Ensure project root is on Python path so all imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
