# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Purpose

DSA study repo organized around the [NeetCode 150](https://neetcode.io/practice) problem set. Solutions are **Python only**; long-form study notes live under `notes/` and build to PDFs via `make`.

For the full project conventions (stub format, README/theory boundary, scripts), see `CLAUDE.md`.
For the day-to-day solving workflow, see `docs/SOLVING.md`.

## Directory Structure

```
dsa/
├── notes/             ← long-form study notes (cheatsheet, ram_model, roadmap, NEETCODE-150)
├── problems/          ← NeetCode 150 solution stubs, grouped by topic
│   ├── 01-arrays-and-hashing/
│   ├── …
│   └── 18-bit-manipulation/
├── scripts/           ← regenerate_stubs.py, progress.py
├── templates/         ← pandoc/LaTeX template (eisvogel)
├── docs/              ← BUILDING.md, SOLVING.md
├── build/             ← generated PDFs (gitignored)
├── pyproject.toml
├── Makefile
└── readme.md
```

Each topic folder under `problems/` contains a `README.md` (theory checklist + problem table), a `theory/notes.md` (deep derivations), and an `exercises/` folder with one Python file per problem. Solution filenames use the LeetCode URL slug in kebab-case, e.g. `exercises/two-sum.py`.

## Common Commands

**Run a solution:**
```bash
python3 problems/01-arrays-and-hashing/exercises/two-sum.py
```

**Update progress counter in `readme.md`:**
```bash
make progress
```

**Re-fetch LeetCode signatures into stubs (network):**
```bash
make regen
```

**Search by problem name:**
```bash
find problems -name "*two-sum*"
```

**Count by status:**
```bash
grep -rl "Status: Stub" problems | wc -l         # unstarted
grep -rl "Status: In-Progress" problems | wc -l  # WIP
grep -rl "Status: Solved" problems | wc -l       # done
```

**Build PDFs from notes:**
```bash
make all          # build everything in notes/ → build/
make pdf          # default: build/ram_model.pdf
make help         # see all targets
```

See `docs/BUILDING.md` for PDF build prerequisites (mactex, pandoc, font setup) and `docs/SOLVING.md` for the solving workflow.
