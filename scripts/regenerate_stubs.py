#!/usr/bin/env python3
"""
Regenerate problem stubs with real LeetCode signatures and runnable example blocks.

Usage:
  python scripts/regenerate_stubs.py                # all problems
  python scripts/regenerate_stubs.py two-sum        # one problem (by slug)
  python scripts/regenerate_stubs.py --dry-run      # preview without writing

Reads the existing docstring of each stub to preserve user-authored fields
(Problem, Difficulty, Category, LeetCode, Approach, Time/Space Complexity,
Status), and rewrites the file with:
  - the same docstring (Status defaulting to "Stub" if missing)
  - the real Python3 class+method signature from LeetCode
  - a runnable `if __name__ == "__main__":` block with example test cases

Problems that fail to fetch (paid-only, removed, slug mismatch) are logged and
skipped — the existing stub is left untouched.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

GRAPHQL = "https://leetcode.com/graphql/"
QUERY = (
    "query q($s: String!) { question(titleSlug: $s) { titleSlug title difficulty"
    " isPaidOnly codeSnippets { langSlug code } exampleTestcases metaData } }"
)

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"

DOCSTRING_FIELDS = (
    "Problem",
    "Difficulty",
    "Category",
    "LeetCode",
    "Status",
    "Approach",
    "Time Complexity",
    "Space Complexity",
)


def fetch(slug: str) -> dict:
    payload = json.dumps({"query": QUERY, "variables": {"s": slug}}).encode()
    req = urllib.request.Request(
        GRAPHQL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://leetcode.com/problems/{slug}/",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    if data.get("errors") or not data.get("data", {}).get("question"):
        raise RuntimeError(f"empty response for {slug}: {data!r}")
    return data["data"]["question"]


def parse_existing_docstring(path: Path) -> dict[str, str]:
    """Pull existing docstring fields. The Approach field is multi-line: it captures
    everything between 'Approach:' and the next single-line field (typically
    'Time Complexity:')."""
    text = path.read_text()
    # Extract everything between the first pair of triple quotes.
    m = re.search(r'"""(.*?)"""', text, re.DOTALL)
    if not m:
        return {}
    body = m.group(1)
    fields: dict[str, str] = {}

    single_line = ("Problem", "Difficulty", "Category", "LeetCode", "Status",
                   "Time Complexity", "Space Complexity")
    for key in single_line:
        m2 = re.search(rf"^\s*{re.escape(key)}:\s*(.*)$", body, re.MULTILINE)
        if m2:
            fields[key] = m2.group(1).strip()

    # Approach: multi-line, ends at "Time Complexity:" or end of docstring.
    m3 = re.search(r"^\s*Approach:\s*\n(.*?)(?=^\s*Time Complexity:|\Z)",
                   body, re.MULTILINE | re.DOTALL)
    if m3:
        fields["Approach"] = m3.group(1).strip("\n")
    return fields


def extract_python_snippet(snippets: list[dict]) -> tuple[str | None, str | None]:
    """Pick the Python3 snippet. Return (function_name, full_class_code).

    The function name is the first `def` *inside* `class Solution:` — not any
    earlier commented-out definitions (e.g. the TreeNode example LeetCode
    inlines for tree problems)."""
    py = None
    for s in snippets or []:
        if s.get("langSlug") == "python3":
            py = s
            break
    if not py:
        return None, None
    code = py["code"].rstrip()
    fn = None
    in_solution = False
    for line in code.splitlines():
        if re.match(r"^class Solution\b", line):
            in_solution = True
            continue
        if not in_solution:
            continue
        m = re.match(r"^\s+def (\w+)\(", line)
        if m and not line.lstrip().startswith("#"):
            fn = m.group(1)
            break
    return fn, code


def normalize_imports(code: str) -> str:
    """LeetCode snippets sometimes use bare `List[int]` etc. — add `from typing import ...`
    if it's referenced but not imported at the top of the file."""
    referenced: set[str] = set()
    for name in ("List", "Optional", "Dict", "Tuple", "Set"):
        if re.search(rf"\b{name}\[", code):
            referenced.add(name)
    if not referenced:
        return code
    return f"from typing import {', '.join(sorted(referenced))}\n\n\n{code}"


def parse_testcases(testcases_str: str | None, n_params: int) -> list[list[str]]:
    """Each `n_params` consecutive non-empty lines is one test case."""
    if not testcases_str or n_params <= 0:
        return []
    lines = [ln for ln in testcases_str.splitlines() if ln.strip() != ""]
    if len(lines) % n_params != 0:
        return []
    return [lines[i : i + n_params] for i in range(0, len(lines), n_params)]


EXOTIC_TYPES = ("TreeNode", "ListNode", "Node")


def has_exotic_param(meta: dict) -> bool:
    """Tree/list problems need helper code to convert LeetCode's array notation
    into the actual node structure — not something we want to autogenerate.
    Detect those and emit commented-out test cases instead of runnable ones."""
    for p in (meta or {}).get("params", []):
        t = p.get("type", "")
        if any(name in t for name in EXOTIC_TYPES):
            return True
    return any(name in (meta or {}).get("return", {}).get("type", "")
               for name in EXOTIC_TYPES)


def to_python_literal(s: str) -> str:
    """LeetCode test values use JSON-ish syntax with `null/true/false`; map to
    Python literals."""
    s = s.strip()
    s = re.sub(r"\bnull\b", "None", s)
    s = re.sub(r"\btrue\b", "True", s)
    s = re.sub(r"\bfalse\b", "False", s)
    return s


def render_main_block(fn: str | None, cases: list[list[str]], exotic: bool) -> str:
    if not fn or not cases:
        return (
            'if __name__ == "__main__":\n'
            "    # Add example test cases here when implementing.\n"
            "    sol = Solution()\n"
        )
    if exotic:
        # Tree/list problems: show the example inputs but don't try to call —
        # the user needs to construct the node graph manually.
        lines = ['if __name__ == "__main__":', "    sol = Solution()",
                 "    # Build the input structure (TreeNode/ListNode) from these examples,",
                 f"    # then call sol.{fn}(...) and print the result."]
        for params in cases:
            pretty = ", ".join(to_python_literal(p) for p in params)
            lines.append(f"    # Example: {fn}({pretty})")
        return "\n".join(lines) + "\n"

    lines = ['if __name__ == "__main__":', "    sol = Solution()"]
    for params in cases:
        args = ", ".join(to_python_literal(p) for p in params)
        lines.append(f"    print(sol.{fn}({args}))")
    return "\n".join(lines) + "\n"


def render_stub(fields: dict[str, str], code: str | None, fn: str | None,
                cases: list[list[str]], meta: dict | None = None) -> str:
    """Compose the full file: docstring + class + __main__ block."""
    approach = fields.get("Approach", "").strip()
    if approach in ("", "-", "- "):
        approach = "- TODO: describe the approach"

    doc = ['"""']
    doc.append(f"Problem: {fields.get('Problem', '?')}")
    doc.append(f"Difficulty: {fields.get('Difficulty', '?')}")
    doc.append(f"Category: {fields.get('Category', '?')}")
    doc.append(f"LeetCode: {fields.get('LeetCode', '?')}")
    doc.append(f"Status: {fields.get('Status', 'Stub')}")
    doc.append("")
    doc.append("Approach:")
    doc.append(approach)
    doc.append("")
    doc.append(f"Time Complexity: {fields.get('Time Complexity', 'O(?)')}")
    doc.append(f"Space Complexity: {fields.get('Space Complexity', 'O(?)')}")
    doc.append('"""')

    if code:
        body = ensure_function_body(code)
        body = normalize_imports(body)
        exotic = has_exotic_param(meta or {})
        prelude = ""
        if exotic:
            # `TreeNode`/`ListNode` are only declared in a comment by LeetCode,
            # so referencing them in annotations breaks on Python <3.14.
            # `from __future__ import annotations` defers evaluation universally.
            prelude = "from __future__ import annotations\n\n"
        return "\n".join(doc) + "\n\n\n" + prelude + body + "\n\n\n" + render_main_block(fn, cases, exotic)

    # Fallback when fetch failed: keep the original generic stub format.
    return "\n".join(doc) + "\n\n\nclass Solution:\n    def solve(self, *args):\n        # TODO: implement\n        pass\n"


def ensure_function_body(code: str) -> str:
    """LeetCode snippets often have an empty function body (the line after the
    `def …:` is just whitespace). Without an explicit `pass` the file is
    syntactically invalid. Inject `# TODO: implement` + `pass` into any empty
    body."""
    lines = code.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        m = re.match(r"^(\s+)def \w+\(.*?\)(?:\s*->\s*[^:]+)?\s*:\s*$", lines[i])
        if m:
            indent = m.group(1) + "    "
            # Look ahead: is the body empty?
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j == len(lines) or not lines[j].startswith(indent):
                out.append(f"{indent}# TODO: implement")
                out.append(f"{indent}pass")
        i += 1
    return "\n".join(out)


def regenerate_one(path: Path, dry_run: bool = False) -> str:
    slug = path.stem
    fields = parse_existing_docstring(path)
    try:
        q = fetch(slug)
    except Exception as exc:  # noqa: BLE001 - we want to log and continue
        return f"FETCH-FAIL  {slug}: {exc}"

    if q.get("isPaidOnly"):
        return f"SKIP-PAID   {slug} (LeetCode Premium — keeping existing stub)"

    fn, code = extract_python_snippet(q.get("codeSnippets") or [])
    if not code:
        return f"NO-PY3      {slug} (no Python3 snippet returned)"

    meta: dict = {}
    try:
        meta = json.loads(q.get("metaData") or "{}")
    except json.JSONDecodeError:
        pass
    n_params = len(meta.get("params") or [])
    cases = parse_testcases(q.get("exampleTestcases"), n_params)

    new_text = render_stub(fields, code, fn, cases, meta=meta)
    if dry_run:
        return f"DRY         {slug}: would write {len(new_text)} bytes, fn={fn}, cases={len(cases)}"

    path.write_text(new_text)
    return f"OK          {slug}: fn={fn}, cases={len(cases)}"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("slug", nargs="?", help="Regenerate one problem by slug; default: all.")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--delay", type=float, default=0.4, help="Seconds between requests.")
    args = p.parse_args()

    paths = sorted(PROBLEMS.glob("*/exercises/*.py"))
    if args.slug:
        paths = [p for p in paths if p.stem == args.slug]
        if not paths:
            sys.exit(f"no stub found for slug: {args.slug}")

    n_ok = n_fail = n_skip = 0
    for i, path in enumerate(paths, 1):
        result = regenerate_one(path, dry_run=args.dry_run)
        print(f"[{i:>3}/{len(paths)}] {result}")
        if result.startswith("OK") or result.startswith("DRY"):
            n_ok += 1
        elif "SKIP" in result:
            n_skip += 1
        else:
            n_fail += 1
        if i < len(paths):
            time.sleep(args.delay)

    print(f"\nDone: {n_ok} ok, {n_skip} skipped, {n_fail} failed.")
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
