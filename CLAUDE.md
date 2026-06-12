# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

DSA study repo organized around the [NeetCode 150](https://neetcode.io/practice) problem set. Solutions live under `problems/` grouped by topic; long-form study notes (theory, cheatsheets, roadmap) live under `notes/` and build to PDFs.

The repo is **Python-only** for solutions. Notes are Markdown that build to PDF via pandoc + the eisvogel template.

## Directory Structure

```
dsa/
├── notes/             ← long-form study notes (cheatsheet, ram_model, roadmap, NEETCODE-150)
├── problems/          ← NeetCode 150 solution stubs, grouped by topic
│   ├── 01-arrays-and-hashing/
│   ├── 02-two-pointers/
│   ├── …
│   └── 18-bit-manipulation/
├── scripts/           ← regenerate_stubs.py, progress.py
├── templates/         ← pandoc/LaTeX template (eisvogel)
├── docs/              ← BUILDING.md (PDFs), SOLVING.md (workflow)
├── build/             ← generated PDFs (gitignored)
├── pyproject.toml     ← Python config (>=3.11), ruff, pytest
├── Makefile
├── readme.md
└── CLAUDE.md
```

Each topic folder under `problems/` contains:

```
<topic>/
├── README.md          ← quick-ref theory checklist + problem table
├── theory/
│   └── notes.md       ← deep theory: proofs, complexity derivations, patterns
└── exercises/
    └── <slug>.py      ← solution stubs (one per problem)
```

## README vs theory/notes.md — the contract

These two files have different jobs. Stay on the right side of the boundary:

- **`<topic>/README.md`** is for **scanning before solving**. It contains:
  - A checklist of concepts (`- [ ] Indexing in O(1) …`) the reader should already know or revisit before tackling problems in this topic.
  - The problem table (Status, Difficulty, Problem name, link, solution file).
  - Pointers to deep material elsewhere.

  Length: ~40–80 lines. Should fit on one screen.

- **`<topic>/theory/notes.md`** is for **consulting during or after solving**. It contains:
  - Formal definitions (e.g., "An array is a sequence of $n$ elements stored in contiguous memory…").
  - Derivations and proofs (potential method for amortized cost, recurrence solutions, invariants).
  - Patterns with worked examples (e.g., "Frequency counting with a hash map" with a concrete walkthrough).

  Length: 100–200 lines is normal. Heavy on math/code.

When in doubt: if it's a *thing to verify you remember*, README. If it's a *thing to look up*, theory/notes.

## Stub Format

Every stub starts with a docstring containing fixed fields, the real LeetCode signature (auto-fetched, see `scripts/regenerate_stubs.py`), and a runnable `__main__` block:

```python
"""
Problem: Two Sum
Difficulty: Easy
Category: Arrays & Hashing
LeetCode: https://leetcode.com/problems/two-sum/
Status: Stub

Approach:
- TODO: describe the approach

Time Complexity: O(?)
Space Complexity: O(?)
"""


from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # TODO: implement
        pass


if __name__ == "__main__":
    sol = Solution()
    print(sol.twoSum([2,7,11,15], 9))
    print(sol.twoSum([3,2,4], 6))
    print(sol.twoSum([3,3], 6))
```

### Status values

- `Stub` — default for unstarted problems.
- `In-Progress` — actively iterating.
- `Solved` — done. Counted by `make progress`.

### Optional fields

- `Last-Reviewed: YYYY-MM-DD` — when you last did the problem from scratch as a refresher. Drives `make review`. Add manually or with `python scripts/review.py --touch <slug>`.

### Premium problems

Seven NeetCode 150 problems are LeetCode Premium (`encode-and-decode-strings`, `graph-valid-tree`, `number-of-connected-components-in-an-undirected-graph`, `walls-and-gates`, `alien-dictionary`, `meeting-rooms`, `meeting-rooms-ii`). Their stubs keep the generic `def solve(self, *args)` because the GraphQL fetch can't reach them without auth. Write the real signature by hand when solving.

## Scripts

- **`scripts/regenerate_stubs.py`** — fetches Python signatures + example test cases from LeetCode GraphQL and rewrites all stubs (`make regen`). Idempotent: re-running preserves user-edited Approach/Status/complexity fields. Run after adding new problems.
- **`scripts/progress.py`** — walks problems/, counts `Status: Solved` per difficulty, rewrites the progress line in `readme.md` (`make progress`). Use `--check` in pre-commit hooks or CI.
- **`scripts/review.py`** — lists Solved problems sorted by oldest `Last-Reviewed:` field for spaced repetition (`make review`). Use `python scripts/review.py --touch <slug>` to stamp today's date after re-doing a problem.

## File Naming Convention

Solution files: `exercises/{leetcode-slug}.py` — kebab-case matching the LeetCode URL slug.
Example: `exercises/two-sum.py`, `exercises/group-anagrams.py`. The slug must match the URL exactly so `regenerate_stubs.py` can fetch metadata.

## Notes (`notes/`)

- `notes/cheatsheet.md` — Big O rules, Master Theorem, all data structure / algorithm complexity tables.
- `notes/ram_model.md` — full theory reference for the RAM model and asymptotic analysis (~1600 lines, 200KB PDF).
- `notes/roadmap.md` — recommended study path through the 150 problems.
- `notes/NEETCODE-150.md` — canonical problem list with categorization.

Build PDFs with `make all` (output to `build/`). See `docs/BUILDING.md` for prerequisites and `make help` for all targets.

## Running Solutions

```bash
# Run a stub (just executes the __main__ block)
python3 problems/01-arrays-and-hashing/exercises/two-sum.py

# Search by problem name
find problems -name "*two-sum*"

# Count remaining stubs / in-progress / solved
grep -rl "Status: Stub" problems | wc -l
grep -rl "Status: In-Progress" problems | wc -l
grep -rl "Status: Solved" problems | wc -l
```

For the day-to-day solving loop, see `docs/SOLVING.md`.
