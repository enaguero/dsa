#!/usr/bin/env python3
"""
List Solved problems sorted by how long ago you last reviewed them, oldest
first. Use this for spaced-repetition: rotate through old solutions so
patterns stay sharp.

A problem is reviewable if it has `Status: Solved` in its docstring.
The optional `Last-Reviewed: YYYY-MM-DD` field tracks the last review.
Problems with no Last-Reviewed field are listed first (never reviewed).

Usage:
  python scripts/review.py                  # next 10 problems to review
  python scripts/review.py --all            # full ranked list
  python scripts/review.py --touch <slug>   # mark <slug> reviewed today
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"


def parse_doc_field(text: str, key: str) -> str | None:
    m = re.search(rf"^\s*{re.escape(key)}:\s*(.*)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def parse_date(s: str | None) -> dt.date | None:
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def collect_solved() -> list[tuple[Path, dt.date | None]]:
    rows: list[tuple[Path, dt.date | None]] = []
    for path in sorted(PROBLEMS.glob("*/exercises/*.py")):
        text = path.read_text()
        if (parse_doc_field(text, "Status") or "").lower() != "solved":
            continue
        rows.append((path, parse_date(parse_doc_field(text, "Last-Reviewed"))))
    # Never-reviewed first, then oldest reviewed.
    rows.sort(key=lambda r: (r[1] is not None, r[1] or dt.date.min))
    return rows


def touch(slug: str) -> int:
    today = dt.date.today().isoformat()
    matches = list(PROBLEMS.glob(f"*/exercises/{slug}.py"))
    if not matches:
        print(f"no stub found for slug: {slug}", file=sys.stderr)
        return 1
    path = matches[0]
    text = path.read_text()
    if "Last-Reviewed:" in text:
        new_text = re.sub(r"^(\s*Last-Reviewed:).*$",
                          rf"\1 {today}", text, count=1, flags=re.MULTILINE)
    else:
        # Insert after Status: line (or after LeetCode: if no Status).
        for anchor in ("Status:", "LeetCode:"):
            if anchor in text:
                new_text = re.sub(
                    rf"^(\s*{anchor}.*)$",
                    rf"\1\nLast-Reviewed: {today}",
                    text, count=1, flags=re.MULTILINE,
                )
                break
        else:
            print(f"no Status/LeetCode anchor in {path}", file=sys.stderr)
            return 1
    path.write_text(new_text)
    print(f"Marked {slug} reviewed {today}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--all", action="store_true", help="Show full list, not just next 10.")
    p.add_argument("--touch", metavar="SLUG", help="Mark <slug> as reviewed today.")
    args = p.parse_args()

    if args.touch:
        return touch(args.touch)

    rows = collect_solved()
    if not rows:
        print("No problems are marked Solved yet. Solve some, then come back.")
        return 0

    today = dt.date.today()
    limit = len(rows) if args.all else 10
    print(f"Spaced-repetition queue ({len(rows)} solved total, showing {min(limit, len(rows))}):")
    print()
    for path, last in rows[:limit]:
        slug = path.stem
        topic = path.parent.parent.name
        if last is None:
            age = "never reviewed"
        else:
            days = (today - last).days
            age = f"{days}d ago ({last.isoformat()})"
        print(f"  {slug:<40} {topic:<30} {age}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
