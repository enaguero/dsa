"""Shared style for ram_model.md figures.

Every figure module imports from here so the whole set reads as one design:
serif type to match the document's TeX Gyre Pagella body text, a restrained
palette built on the document's link/title colors, no chartjunk.

Figures are saved at a physical size that embeds 1:1 in the PDF (text width
is 6.5in at 1in margins; default figure width 5.5in) and crisply on GitHub.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).resolve().parents[2] / "notes" / "figures"

# Palette anchored to the document: NavyBlue links, #360049 titlepage rule.
INK = "#1a1a2e"  # near-black for primary lines/text
NAVY = "#1f4e8c"  # primary series (document link color family)
PURPLE = "#360049"  # emphasis (document titlepage rule)
ORANGE = "#c2571a"  # contrast series — survives grayscale against navy
TEAL = "#2a7f7f"  # secondary series
GRAY = "#8a8a93"  # de-emphasized series / reference lines
LIGHT = "#e8e8ee"  # fills, bands

# Ordered cycle for multi-series plots (adjacent entries differ in lightness
# so the ordering still reads in grayscale).
SERIES = ["#1f4e8c", "#c2571a", "#2a7f7f", "#360049", "#8a8a93", "#6b9bd1"]


def apply_style() -> None:
    """Set rcParams. Call once at the top of each figure script."""
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["TeX Gyre Pagella", "Palatino", "Georgia", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 9.5,
            "axes.titlesize": 10.5,
            "axes.labelsize": 9.5,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "legend.fontsize": 8.5,
            "legend.frameon": False,
            "grid.color": LIGHT,
            "grid.linewidth": 0.6,
            "lines.linewidth": 1.6,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig: plt.Figure, slug: str) -> Path:
    """Save under notes/figures/<slug>.png at print-quality DPI."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out = FIGURES_DIR / f"{slug}.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"wrote {out}")
    return out
