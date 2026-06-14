"""Limit-line analogy for O / Omega / Theta / little-o / little-omega (§8.3).

A number line in L = lim f(n)/g(n). The three landmark regions sort the
five asymptotic relations, and two stacked brackets show that O and Omega
are overlapping half-lines whose intersection is exactly Theta.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyBboxPatch, Rectangle

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, PURPLE, apply_style, save


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.0, 5.0)
    ax.set_aspect("auto")
    ax.axis("off")

    # ---- number line of L ------------------------------------------------
    line_y = 3.9
    L0, LMID, LINF = 1.2, 5.0, 8.8

    ax.annotate(
        "",
        xy=(LINF + 0.6, line_y), xytext=(L0 - 0.6, line_y),
        arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK),
    )
    ax.text(L0 - 0.85, line_y, r"$L = \lim_{n\to\infty} f(n)/g(n)\!:$",
            ha="right", va="center", fontsize=9.5, color=INK)

    # landmark ticks
    for x, label in [(L0, "$0$"), (LINF, r"$\infty$")]:
        ax.plot([x, x], [line_y - 0.10, line_y + 0.10], color=INK, lw=1.3)
        ax.text(x, line_y + 0.20, label, ha="center", va="bottom",
                fontsize=11, color=INK)
    # the open interval (0, infinity) is the whole middle of the line
    ax.fill_between([L0 + 0.04, LINF - 0.04],
                    [line_y - 0.06] * 2, [line_y + 0.06] * 2,
                    color=to_rgba(NAVY, 0.10), zorder=0)
    ax.text(LMID, line_y + 0.20, r"$(0,\,\infty)$",
            ha="center", va="bottom", fontsize=10.5, color=NAVY)

    # ---- relation labels at each landmark --------------------------------
    rel_y = line_y - 0.55
    for x, txt, col in [
        (L0,   r"$f = o(g)$",    PURPLE),
        (LMID, r"$f = \Theta(g)$", NAVY),
        (LINF, r"$f = \omega(g)$", ORANGE),
    ]:
        ax.text(x, rel_y, txt, ha="center", va="top",
                fontsize=10.5, color=col, weight="bold")

    # ---- analogy row -----------------------------------------------------
    analogy_y = rel_y - 0.62
    ax.text(L0 - 0.85, analogy_y, "analogy on reals:",
            ha="right", va="center", fontsize=9, style="italic", color=GRAY)
    for x, sym in [(L0, r"$<$"), (LMID, r"$=$"), (LINF, r"$>$")]:
        ax.text(x, analogy_y, sym, ha="center", va="center",
                fontsize=14, color=GRAY)

    # ---- O bracket: covers L = 0 through (0, ∞) --------------------------
    o_y = 1.85
    o_x0, o_x1 = L0 - 0.30, LMID + 1.30
    ax.add_patch(Rectangle((o_x0, o_y - 0.16), o_x1 - o_x0, 0.32,
                           fc=to_rgba(NAVY, 0.10), ec=NAVY, lw=1.0))
    ax.text(o_x0 - 0.15, o_y, r"$f = O(g)$   $(\leq):$",
            ha="right", va="center", fontsize=9.5, color=INK)
    # Labels off the overlap rectangle — anchored on the unique-to-O side
    ax.text((o_x0 + L0 + 0.40) / 2, o_y, r"$o(g)$",
            ha="center", va="center", fontsize=9.5, color=NAVY,
            weight="bold")

    # ---- Omega bracket: covers (0, ∞) through L = ∞ ----------------------
    om_y = 0.95
    om_x0, om_x1 = LMID - 1.30, LINF + 0.30
    ax.add_patch(Rectangle((om_x0, om_y - 0.16), om_x1 - om_x0, 0.32,
                           fc=to_rgba(ORANGE, 0.10), ec=ORANGE, lw=1.0))
    ax.text(om_x0 - 0.15, om_y, r"$f = \Omega(g)$   $(\geq):$",
            ha="right", va="center", fontsize=9.5, color=INK)
    # Labels off the overlap rectangle — anchored on the unique-to-Ω side
    ax.text((LINF - 0.40 + om_x1) / 2, om_y, r"$\omega(g)$",
            ha="center", va="center", fontsize=9.5, color=ORANGE,
            weight="bold")

    # ---- overlap = Theta -------------------------------------------------
    over_x0 = max(o_x0, om_x0)
    over_x1 = min(o_x1, om_x1)
    over_y0, over_y1 = om_y - 0.18, o_y + 0.18
    ax.add_patch(Rectangle((over_x0, over_y0),
                           over_x1 - over_x0, over_y1 - over_y0,
                           fc=to_rgba(PURPLE, 0.14), ec=PURPLE,
                           lw=1.4, ls=(0, (3, 2))))
    # Theta label inside the overlap rectangle
    ax.text((over_x0 + over_x1) / 2, (over_y0 + over_y1) / 2,
            r"$\Theta(g)$",
            ha="center", va="center", fontsize=11, weight="bold",
            color=PURPLE)

    # caption box for the overlap
    cap_x = (over_x0 + over_x1) / 2
    cap_y = 0.25
    ax.add_patch(FancyBboxPatch((cap_x - 1.85, cap_y - 0.20), 3.7, 0.42,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc=LIGHT, ec=PURPLE, lw=1.0))
    ax.text(cap_x, cap_y,
            r"overlap $=\;\Theta\;=\;O \cap \Omega$",
            ha="center", va="center", fontsize=10, color=PURPLE,
            weight="bold")
    # connector from overlap rectangle down to caption box
    ax.plot([cap_x, cap_x], [over_y0 - 0.02, cap_y + 0.22],
            color=PURPLE, lw=0.8, ls=":")

    save(fig, "limit-line-asymptotic-relations")


if __name__ == "__main__":
    main()
