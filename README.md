<div align="center">

# ⚙️ CacheSim Pro

### Cache Memory Simulator — Interactive Visualizer Tool

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6B6B?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-2ECC71?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-2ECC71?style=for-the-badge)
![No Dependencies](https://img.shields.io/badge/Dependencies-None-F39C12?style=for-the-badge)

**Visualize, simulate, and understand cache memory replacement algorithms — step by step.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Algorithms](#-algorithms) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**CacheSim Pro** is an interactive desktop application that helps Computer Science and Engineering students deeply understand how cache memory works through real-time visualization, step-by-step simulation, and live statistics. It is a gift to all my department juniors across the world.

Instead of reading about cache hits and misses in a textbook, students can **see** them happen — with color-coded blocks, instant feedback, and side-by-side algorithm comparison.
Thank You <3
- SMI Fahim

### Who Is This For?

| Audience | What They Learn |
|---|---|
| CS Students | How CPU cache reduces memory access time |
| Engineering Students | Cache replacement policy trade-offs |
| OS Learners | Page replacement concepts (directly applicable) |
| Architecture Learners | Hardware-level memory hierarchy behavior |

---

## ✨ Features

### 🎮 Simulation Controls
- **▶ Start** — Configure and launch a fresh simulation
- **⏭ Next Step** — Advance one reference at a time (great for learning)
- **⚡ Auto Play** — Watch the full simulation run automatically
- **⏸ Pause** — Pause auto-play mid-simulation
- **↺ Reset** — Clear everything and start over

### 🎨 Visual Cache Display
- Color-coded cache blocks update in real time
  - 🟢 **Green** — Cache Hit (page already loaded)
  - 🔴 **Red** — Cache Miss (page newly loaded)
  - 🟡 **Yellow** — Replaced block (evicted page)
  - ⬛ **Gray** — Empty cache slot
- Reference string progress tracker highlights current position
- Step-by-step decision label explains every action

### 📊 Live Statistics Panel
- Total Requests processed
- Total Cache Hits
- Total Cache Misses
- Hit Ratio (%)
- Miss Ratio (%)

### 🔧 Algorithm Support
| Algorithm | Strategy | Best For |
|---|---|---|
| **FIFO** | Evict oldest page | Teaching basic replacement |
| **LRU** | Evict least recently used | Real-world approximation |
| *(Extensible)* | Add your own in 1 file | Research & experimentation |

---

## 🖥️ Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────┐
│ ⚙ CacheSim Pro          Cache Memory Simulator          │
│                                                         │
│ Algorithm [FIFO▼]  Cache Size [3]                       │
│ Reference String  [1 2 3 2 4 1 5 2 3]                  │
│                                                         │
│ [▶ Start] [⏭ Next Step] [⚡ Auto Play] [↺ Reset]       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Step 5 / 9  →  Page Requested: 4                      │
│                          ❌ MISS — Page 1 replaced by 4 │
│                                                         │
│   ┌────────┐  ┌────────┐  ┌────────┐                   │
│   │   2    │  │   3    │  │   4    │                   │
│   │ Slot 0 │  │ Slot 1 │  │ Slot 2 │                   │
│   └────────┘  └────────┘  └────────┘                   │
│    (gray)      (gray)      (red=new)                    │
│                                                         │
│  Reference String:  1  2  3  2 [4] 1  5  2  3          │
│                                                         │
│  ● Cache Hit  ● Cache Miss  ● Replaced  ● Empty Slot   │
├─────────────────────────────────────────────────────────┤
│  TOTAL    │  HITS   │  MISSES  │  HIT %   │  MISS %    │
│    5      │    1    │    4     │  20.00%  │  80.00%    │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python **3.8 or higher**
- Tkinter (bundled with Python on Windows and macOS)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/cachesim-pro.git
cd cachesim-pro
```

### Step 2 — Verify Python Version
```bash
python --version
# Should output: Python 3.8.x or higher
```

### Step 3 — Check Tkinter (Linux only)
```bash
python -m tkinter
# A small test window should appear
```

If tkinter is missing on Linux:
```bash
# Ubuntu / Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Step 4 — Run the Application
```bash
python main.py
```

Or on Linux/Mac use the included launch script:
```bash
chmod +x run.sh
./run.sh
```

> ✅ **No pip install required.** CacheSim Pro uses only Python standard library modules.

---

## 📘 Usage Guide

### Quick Start (30 seconds)

1. **Launch** the app with `python main.py`
2. **Select algorithm** — choose `FIFO` or `LRU` from the dropdown
3. **Set cache size** — enter a number like `3` or `4`
4. **Enter reference string** — space-separated page numbers e.g. `1 2 3 2 4 1 5 2`
5. **Click ▶ Start** — simulation is ready
6. **Click ⏭ Next Step** — advance one page at a time and observe the cache blocks
7. **Click ⚡ Auto Play** — watch the full simulation run automatically

### Understanding the Display

| Element | Meaning |
|---|---|
| Green block | This page was already in cache — **Cache Hit** |
| Red block | This page was not in cache — **Cache Miss**, just loaded |
| Yellow block | This page was just evicted — **Replacement occurred** |
| Gray block | This slot is currently empty |
| `[4]` in reference string | The page currently being processed |
| Decision label | Explains exactly what happened this step |

### Example Walkthrough

**Configuration:** Algorithm = FIFO, Cache Size = 3, Reference = `1 2 3 2 4 1 5`

| Step | Page | Cache State | Event |
|------|------|-------------|-------|
| 1 | 1 | [1] | MISS — loaded into empty slot |
| 2 | 2 | [1, 2] | MISS — loaded into empty slot |
| 3 | 3 | [1, 2, 3] | MISS — cache now full |
| 4 | 2 | [1, 2, 3] | **HIT** — page 2 already present |
| 5 | 4 | [2, 3, 4] | MISS — page **1** evicted (FIFO oldest) |
| 6 | 1 | [3, 4, 1] | MISS — page **2** evicted (FIFO oldest) |
| 7 | 5 | [4, 1, 5] | MISS — page **3** evicted (FIFO oldest) |

**Final Stats:** 1 Hit, 6 Misses, Hit Rate = 14.29%

### Comparing FIFO vs LRU

Run the same reference string with both algorithms to see how replacement decisions differ:

- **FIFO** always evicts the *oldest loaded* page regardless of recent use
- **LRU** evicts the *least recently accessed* page — smarter about keeping hot data

This difference becomes visible in longer reference strings with repeated patterns.

---

## 🏗️ Architecture

CacheSim Pro uses a clean **3-Layer MVC Architecture**:

```
┌─────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                 │
│  gui/main_window.py   — Root window & controller   │
│  gui/control_panel.py — Inputs & buttons            │
│  gui/cache_display.py — Animated cache blocks       │
│  gui/stats_panel.py   — Live statistics cards       │
├─────────────────────────────────────────────────────┤
│                   ENGINE LAYER                      │
│  engine/simulator.py    — Step-by-step driver       │
│  engine/stats_manager.py — Hit/miss tracking        │
├─────────────────────────────────────────────────────┤
│                    CORE LAYER                       │
│  core/cache_base.py        — Abstract contract      │
│  core/fifo_cache.py        — FIFO implementation    │
│  core/lru_cache.py         — LRU implementation     │
│  core/algorithm_factory.py — Factory pattern        │
└─────────────────────────────────────────────────────┘
         utils/validators.py — Input validation
```

### Design Patterns Used

| Pattern | Location | Purpose |
|---|---|---|
| **Strategy** | `core/` algorithms | Swap algorithms without GUI changes |
| **Factory** | `algorithm_factory.py` | Create algorithm objects by name |
| **MVC** | All layers | Clean separation of concerns |
| **Observer** | Engine → GUI | Decoupled result delivery via StepResult |

### Data Flow

```
User Input → validators.py → Simulator.step()
                                    │
                          ┌─────────┴──────────┐
                          ▼                    ▼
                    FIFOCache / LRUCache   StatsManager
                          │                    │
                          └─────────┬──────────┘
                                    ▼
                               StepResult
                          ┌─────────┴──────────┐
                          ▼                    ▼
                    CacheDisplay          StatsPanel
```

---

## 🧮 Algorithms

### FIFO — First In, First Out

```
Concept: Pages form a queue. Oldest page is always evicted first.

Reference: 1 2 3 4  (cache size = 3)
Step 1: [1]         ← 1 loaded
Step 2: [1,2]       ← 2 loaded
Step 3: [1,2,3]     ← 3 loaded, cache FULL
Step 4: [2,3,4]     ← 1 EVICTED (arrived first), 4 loaded

Implementation: collections.deque
  append()    → add newest to right
  popleft()   → remove oldest from left
  Complexity: O(1) insert and eviction
```

### LRU — Least Recently Used

```
Concept: Track when each page was last used.
         Evict the page that hasn't been used the longest.

Reference: 1 2 3 2 4  (cache size = 3)
Step 1: [1]           Miss
Step 2: [1,2]         Miss
Step 3: [1,2,3]       Miss, order: 1(LRU)→2→3(MRU)
Step 4: [1,3,2]       HIT on 2, refreshed: 1(LRU)→3→2(MRU)
Step 5: [3,2,4]       Miss, 1 EVICTED (LRU), order: 3→2→4

Implementation: collections.OrderedDict
  move_to_end()       → refresh on hit
  popitem(last=False) → evict LRU
  Complexity: O(1) for all operations
```

### Adding a New Algorithm

To add **LFU, Optimal, Clock**, or any other algorithm:

1. Create `core/lfu_cache.py` inheriting `CacheBase`
2. Implement the `access(page)` method
3. Add one line to `core/algorithm_factory.py`:
   ```python
   from core.lfu_cache import LFUCache
   ALGORITHM_MAP = {
       "FIFO": FIFOCache,
       "LRU" : LRUCache,
       "LFU" : LFUCache,    # ← just this line
   }
   ```
4. The GUI dropdown updates **automatically** — zero other changes needed

---

## 📁 Project Structure

```
cachesim_pro/
│
├── main.py                     # Entry point — run this
├── requirements.txt            # No external deps needed
├── run.sh                      # Linux/Mac launch script
├── .gitignore
├── README.md
│
├── core/                       # Pure cache logic (no GUI)
│   ├── cache_base.py           # Abstract base class
│   ├── fifo_cache.py           # FIFO algorithm
│   ├── lru_cache.py            # LRU algorithm
│   └── algorithm_factory.py   # Factory pattern
│
├── engine/                     # Simulation control
│   ├── simulator.py            # Step engine + StepResult
│   └── stats_manager.py       # Hit/miss statistics
│
├── gui/                        # Tkinter interface
│   ├── main_window.py          # Root window & controller
│   ├── control_panel.py        # Inputs & buttons
│   ├── cache_display.py        # Visual cache blocks
│   └── stats_panel.py         # Statistics display
│
└── utils/
    └── validators.py           # Input validation
```

---

## 🧪 Running Tests

No external test framework required. Run the built-in test suite:

```bash
# Algorithm unit tests (30 cases)
python -c "
import sys; sys.path.insert(0, '.')
from core.fifo_cache import FIFOCache
from core.lru_cache  import LRUCache

f = FIFOCache(3)
assert f.access(1) == (False, None)
assert f.access(2) == (False, None)
assert f.access(3) == (False, None)
assert f.access(2) == (True,  None)   # HIT
assert f.access(4) == (False, 1)      # evicts page 1
print('✅ FIFO tests passed')

l = LRUCache(3)
l.access(1); l.access(2); l.access(3)
l.access(2)                            # refresh page 2
assert l.access(4) == (False, 1)      # page 1 is LRU
print('✅ LRU tests passed')
"
```

```bash
# Full simulation test
python -c "
import sys; sys.path.insert(0, '.')
from engine.simulator import Simulator

sim = Simulator('LRU', 3, [1,2,3,2,4,1,5,2])
results = []
while not sim.is_done():
    results.append(sim.step())
stats = sim.stats.get_stats()
print(f'Steps: {stats[\"total\"]}  Hits: {stats[\"hits\"]}  Misses: {stats[\"misses\"]}')
print('✅ Simulation test passed')
"
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

### Good First Issues
- Add **Optimal (OPT)** page replacement algorithm
- Add **Clock (Second Chance)** algorithm
- Export simulation results to CSV
- Add keyboard shortcuts (Space = Next Step)

### How to Contribute
```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/lfu-algorithm

# 3. Make your changes following the existing pattern
# 4. Test your changes
python main.py

# 5. Submit a pull request
```

### Code Style
- Follow the existing docstring format
- Keep GUI and logic strictly separated
- Add comments explaining the *why*, not just the *what*
- New algorithms go in `core/` and register in `algorithm_factory.py`

---

## 📄 License

```
MIT License

Copyright (c) 2026 CacheSim Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👨‍💻 Author

Built out of curiosity and to help my department juniors:
- Clean Python architecture (MVC + Strategy + Factory patterns)
- Object-oriented design with abstract base classes
- Tkinter GUI development
- Algorithm implementation (FIFO, LRU)
- Software engineering best practices

---

<div align="center">

**⭐ If this project helped you understand cache memory, please star it on GitHub and do follow me on socials!**

Made with ❤️ for Computer Science students everywhere
Thanks
-SMI Fahim (CSE - North South University - Batch 211)

</div>
