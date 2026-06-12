#!/usr/bin/env python3
"""
Walk problems/, count solved-vs-total per difficulty, rewrite the progress line
in readme.md.

A problem counts as "Solved" if its docstring contains `Status: Solved`. Stubs
default to `Status: Stub`. Anything else (e.g. `In-Progress`) counts as
unsolved for progress purposes.

Usage:
  python scripts/progress.py            # update readme.md in place
  python scripts/progress.py --check    # exit non-zero if readme.md is stale
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"
README = ROOT / "readme.md"

PROGRESS_LINE_RE = re.compile(
    r"^\*\*Progress: \d+ / \d+\*\*[^\n]*$",
    re.MULTILINE,
)


def parse_doc_field(text: str, key: str) -> str | None:
    m = re.search(rf"^\s*{re.escape(key)}:\s*(.*)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def collect_counts() -> tuple[Counter[str], Counter[str]]:
    """Return (totals_by_difficulty, solved_by_difficulty)."""
    total: Counter[str] = Counter()
    solved: Counter[str] = Counter()
    for path in sorted(PROBLEMS.glob("*/exercises/*.py")):
        text = path.read_text()
        diff = parse_doc_field(text, "Difficulty") or "Unknown"
        status = parse_doc_field(text, "Status") or "Stub"
        total[diff] += 1
        if status.lower() == "solved":
            solved[diff] += 1
    return total, solved


def render_line(total: Counter[str], solved: Counter[str]) -> str:
    grand = sum(total.values())
    grand_solved = sum(solved.values())
    parts = [f"**Progress: {grand_solved} / {grand}**"]
    for diff in ("Easy", "Medium", "Hard"):
        parts.append(f"{diff}: {solved.get(diff, 0)} / {total.get(diff, 0)}")
    return " &nbsp;|&nbsp; ".join(parts)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true",
                   help="Exit non-zero if readme.md is out of date.")
    args = p.parse_args()

    total, solved = collect_counts()
    new_line = render_line(total, solved)

    text = README.read_text()
    if not PROGRESS_LINE_RE.search(text):
        print(f"error: no progress line matching {PROGRESS_LINE_RE.pattern!r} in {README}",
              file=sys.stderr)
        return 2

    new_text = PROGRESS_LINE_RE.sub(new_line, text, count=1)

    if args.check:
        if new_text != text:
            print("readme.md progress line is stale. Run: python scripts/progress.py")
            print(f"  expected: {new_line}")
            return 1
        print("readme.md is up to date.")
        return 0

    if new_text == text:
        print(f"No change. Current: {new_line}")
        return 0

    README.write_text(new_text)
    print(f"Updated readme.md: {new_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
