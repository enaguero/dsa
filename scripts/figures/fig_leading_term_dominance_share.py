"""Stacked-share chart: each term of T(n) = 4n^3 + 17n^2 log n + 100n + 250 dominates in turn, then the leading term takes over (section 6, Why We Need Asymptotic Notation)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from _style import INK, NAVY, apply_style, save


def main() -> None:
    apply_style()
    import matplotlib.pyplot as plt

    n = np.logspace(0, 4, 2000)
    t1 = np.full_like(n, 250.0)
    t2 = 100.0 * n
    t3 = 17.0 * n**2 * np.log2(np.maximum(n, 1.0))
    t4 = 4.0 * n**3
    total = t1 + t2 + t3 + t4
    shares = [t1 / total, t2 / total, t3 / total, t4 / total]

    # First n where the leading term alone is >= 90% of the total.
    n_star = n[np.argmax(shares[3] >= 0.9)]

    fig, ax = plt.subplots(figsize=(5.6, 3.3))

    grays = ["#e1e1e1", "#bdbdbd", "#949494"]  # light -> dark, bottom three terms
    ax.stackplot(n, shares, colors=grays + [NAVY], edgecolor="white", linewidth=0.7)

    ax.set_xscale("log")
    ax.set_xlim(1, 1e4)
    ax.set_xticks([1, 10, 100, 1000, 10000], ["$1$", "$10$", "$10^2$", "$10^3$", "$10^4$"])
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.5, 1.0], ["0%", "50%", "100%"])
    ax.set_xlabel("$n$ (log scale)")
    ax.set_ylabel("share of $T(n)$")
    ax.set_title(r"Term-by-term share of $T(n) = 4n^3 + 17n^2 \log n + 100n + 250$")

    # Label each band inside it, at (near) its widest point.
    ax.text(1.5, 0.29, "$250$", ha="center", va="center", color=INK)
    ax.text(2.2, 0.60, "$100n$", ha="center", va="center", color=INK)
    ax.text(10, 0.38, r"$17n^2 \log n$", ha="center", va="center", color=INK)
    ax.text(900, 0.58, "$4n^3$", ha="center", va="center", color="white", fontsize=15)

    # Threshold where the leading term reaches 90% of the runtime.
    ax.axvline(n_star, color="white", linestyle=(0, (1, 2.2)), linewidth=1.1)
    ax.text(
        n_star * 1.18,
        0.24,
        "leading term ≥ 90% of\n" f"runtime from $n \\approx {n_star:.0f}$ on",
        ha="left",
        va="center",
        color="white",
        fontsize=8,
        linespacing=1.5,
    )

    save(fig, "leading-term-dominance-share")


if __name__ == "__main__":
    main()
