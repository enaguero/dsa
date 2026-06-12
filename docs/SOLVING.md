# Solving Workflow

This document is the answer to "what do I do first?" when sitting down to solve a problem in this repo.

## One-time setup

```bash
# Pick a Python (3.11+).
python3 --version

# Install dev dependencies (pytest + ruff).
pip install -e ".[dev]"
# or, with uv:
uv sync
```

That's it. No build step is needed for solving problems — only for compiling notes to PDF (see `docs/BUILDING.md`).

## The solving loop

1. **Pick a problem.** `notes/roadmap.md` lists the recommended order through NeetCode 150. Each topic's `problems/<topic>/README.md` has the per-topic table.

2. **Open the stub.** Every stub already has the real LeetCode method signature, the example test cases as runnable `print(...)` calls, and a `Status: Stub` field in the docstring.

   ```bash
   $EDITOR problems/01-arrays-and-hashing/exercises/two-sum.py
   ```

3. **Read the problem statement** at the LeetCode URL in the docstring header. Skim the topic theory first if you're shaky on the patterns:

   ```bash
   less problems/01-arrays-and-hashing/theory/notes.md
   ```

4. **Write the solution.** Replace the `# TODO: implement` + `pass` lines. Update the docstring as you go:
   - `Approach:` — one or two sentences on what your solution does.
   - `Time Complexity:` / `Space Complexity:` — fill in the real bounds.
   - `Status:` — change to `In-Progress` while iterating, `Solved` when done and tested.

5. **Run it.** The example test cases print outputs. Compare against the LeetCode problem statement's expected output.

   ```bash
   python3 problems/01-arrays-and-hashing/exercises/two-sum.py
   ```

6. **Mark solved + update the progress counter.** When you're satisfied:

   ```bash
   make progress
   ```

   That walks `problems/`, counts everything with `Status: Solved`, and rewrites the line in `readme.md`. Commit both the solution and the updated readme together.

## Status field values

The `Status:` line in each docstring takes one of:

- **`Stub`** — never opened, starting state. Counted as unsolved.
- **`In-Progress`** — actively working on it. Counted as unsolved.
- **`Solved`** — done and tested. Counted as solved.

`make progress` and `python3 scripts/progress.py --check` both rely on this field, so keep it accurate.

## Tree and linked-list problems

Stubs with `TreeNode` or `ListNode` parameters have their `__main__` block as commented examples instead of executable calls — LeetCode test cases use array notation that you must convert to a node graph yourself. The commented examples show the input shape; build the tree/list manually inside `__main__` to test:

```python
if __name__ == "__main__":
    sol = Solution()
    # Example: maxPathSum([1,2,3])
    # Example: maxPathSum([-10,9,20,None,None,15,7])
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    print(sol.maxPathSum(root))
```

There is no `TreeNode` / `ListNode` class shipped with the stubs (LeetCode includes one as a comment). Define the obvious one inside the file when you start solving, or factor a `_common.py` helper if you find yourself repeating it.

## Common make targets

| Command | What it does |
|---|---|
| `make progress` | Recompute the progress line in `readme.md` |
| `make review` | List solved problems by oldest `Last-Reviewed` (spaced repetition) |
| `make regen` | Re-fetch LeetCode signatures into stubs (only for new/Premium-fixed problems) |
| `make pdf` | Build `notes/ram_model.md` → `build/ram_model.pdf` |
| `make all` | Build all notes to PDFs |
| `make help` | Full target list |

## Spaced repetition

After solving a problem, optionally add `Last-Reviewed: YYYY-MM-DD` to its docstring. Then `make review` shows your solved problems sorted by oldest review (or never reviewed) — pick the top one and re-derive it from scratch. When done, stamp today's date:

```bash
python3 scripts/review.py --touch two-sum
```

This is opt-in. If you don't add `Last-Reviewed` fields, `make review` just lists Solved problems in filename order.

## Search and stats

```bash
# Find a problem by partial name
find problems -name "*two-sum*"

# Count remaining stubs
grep -rl "Status: Stub" problems | wc -l

# List all in-progress problems
grep -rl "Status: In-Progress" problems

# What problems are LeetCode Premium (skipped by regen)?
grep -rL "from typing" problems/*/exercises/*.py | head
```

## When you finish a topic

Tag it. Cheap, motivating:

```bash
git tag arrays-complete   # or trees-complete, dp-complete, …
git push --tags
```

## Premium problems

Seven problems in NeetCode 150 are LeetCode Premium and can't be auto-fetched: `encode-and-decode-strings`, `graph-valid-tree`, `number-of-connected-components-in-an-undirected-graph`, `walls-and-gates`, `alien-dictionary`, `meeting-rooms`, `meeting-rooms-ii`. Their stubs use the generic `def solve(self, *args)` signature — write the real signature manually when solving.
