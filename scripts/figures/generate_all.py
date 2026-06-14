"""Regenerate every figure for notes/ram_model.md.

Each fig_*.py module in this directory is a standalone script that writes one
PNG to notes/figures/. This driver just runs them all:

    uv run --with matplotlib python scripts/figures/generate_all.py   # or: make figures

Figures are committed (notes/figures/ is not gitignored) so the markdown
renders on GitHub without a build step; rerun this only when a figure changes.
"""

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    scripts = sorted(HERE.glob("fig_*.py"))
    if not scripts:
        print("no fig_*.py scripts found", file=sys.stderr)
        return 1
    for script in scripts:
        print(f"-- {script.name}")
        runpy.run_path(str(script), run_name="__main__")
    print(f"{len(scripts)} figures regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
