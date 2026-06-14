"""Growth-rate hierarchy on log-log axes (§11): polynomials are straight lines, 2^n is not."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from _style import GRAY, INK, NAVY, ORANGE, apply_style, save

YTOP = 1e13
ONE_SECOND = 1e9  # ops budget for "one second" (§11.3)


def main() -> None:
    apply_style()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.0, 4.45))

    n = np.logspace(0, 6, 500)

    # Sub-linear classes: gray, broken linestyles.
    ax.plot(n, np.ones_like(n), color=GRAY, ls=":", lw=1.4)
    ax.plot(n, np.log2(n), color=GRAY, ls="--", lw=1.4)
    ax.plot(n, np.sqrt(n), color=GRAY, ls=(0, (6, 2)), lw=1.4)

    # Polynomial classes: navy, solid — straight lines on log-log axes.
    for f in (n, n * np.log2(n), n**2, n**3):
        ax.plot(n, f, color=NAVY, ls="-", lw=1.6)

    # Exponential: orange dash-dot; compute only where it fits in float range
    # and let the curve exit through the top of the axes.
    n_exp = n[n <= 50]
    ax.plot(n_exp, 2.0**n_exp, color=ORANGE, ls="-.", lw=2.0)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1e6)
    ax.set_ylim(0.8, YTOP)
    ax.set_xlabel("$n$  (log scale)")
    ax.set_ylabel("operations  (log scale)")
    ax.grid(True, which="major", axis="both")
    ax.set_axisbelow(True)

    # Direct end-of-line labels at the right edge, ascending order.
    nmax = 1e6
    right_labels = [
        ("$1$", 1.0, GRAY),
        ("$\\log n$", np.log2(nmax), GRAY),
        ("$\\sqrt{n}$", np.sqrt(nmax), GRAY),
        ("$n$", nmax, NAVY),
        ("$n\\,\\log n$", nmax * np.log2(nmax), NAVY),
        ("$n^2$", nmax**2, NAVY),
    ]
    for text, y, color in right_labels:
        ax.text(1.22e6, y, text, color=color, fontsize=10,
                ha="left", va="center", clip_on=False)

    # Curves that escape through the top edge: label at their exit x.
    x_exit_cubic = YTOP ** (1 / 3)          # n^3 = YTOP
    x_exit_exp = np.log2(YTOP)              # 2^n = YTOP
    ax.text(x_exit_cubic, YTOP * 1.8, "$n^3$", color=NAVY, fontsize=10,
            ha="center", va="bottom", clip_on=False)
    ax.text(x_exit_exp, YTOP * 1.8, "$2^n$", color=ORANGE, fontsize=10,
            ha="center", va="bottom", clip_on=False)
    ax.annotate(
        "$2^n$ exits the chart\nby $n \\approx 40$",
        xy=(x_exit_exp * 1.25, YTOP * 0.55), xytext=(320, 6e11),
        color=ORANGE, fontsize=9, ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9,
                        shrinkA=2, shrinkB=2),
    )

    # One-second budget: ~10^9 ops (§11.3). Crossings reproduce the table.
    ax.axhline(ONE_SECOND, color=GRAY, ls=(0, (1, 3)), lw=1.1)
    ax.text(1.25, ONE_SECOND * 1.7, "$\\approx 10^9$ ops $\\approx$ one second",
            color=GRAY, fontsize=8.5, ha="left", va="bottom")
    crossings = [  # (x where curve = 10^9, label below marker)
        (np.log2(ONE_SECOND), "$n \\approx 30$"),         # 2^n
        (ONE_SECOND ** (1 / 3), "$n \\approx 10^3$"),     # n^3
        (np.sqrt(ONE_SECOND), "$n \\approx 3{\\cdot}10^4$"),  # n^2
    ]
    for x, label in crossings:
        ax.plot([x], [ONE_SECOND], marker="o", ms=4.5, mfc="white",
                mec=INK, mew=1.0, ls="none", zorder=5)
        ax.text(x, ONE_SECOND / 2.6, label, color=INK, fontsize=7.5,
                ha="center", va="top")

    # The reading aid for the whole figure, set inside the wedge between the
    # n and sqrt(n) lines and rotated to run parallel to them (slope 0.75 in
    # log-log coordinates, converted to a screen angle through transData).
    p1 = ax.transData.transform((1e3, 1e3**0.75))
    p2 = ax.transData.transform((1e6, 1e6**0.75))
    angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
    xc = 3e4
    ax.text(
        xc, xc**0.75,
        "log–log axes: every polynomial $n^k$\nis a straight line of slope $k$",
        color=INK, fontsize=8.5, ha="center", va="center",
        rotation=angle, rotation_mode="anchor",
    )

    save(fig, "growth-rate-hierarchy-loglog")


if __name__ == "__main__":
    main()
