"""Binary counter amortized trace under the potential method (ram_model.md §19.4).

Eight increments of a 4-bit counter visualised as: (a) a clean tabular grid
of the counter state at each step with flipped bits highlighted plus columns
for actual cost, dPhi and amortized, and (b) a chart that lays the actual
cost (bars), potential (zigzag), and amortized = 2 (flat line) on top of one
another so the expensive carry chain at step 8 lines up exactly with the
potential crash that pays for it.

This is the algebra (t+1) + (1-t) = 2 happening in real numbers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle

from _style import GRAY, INK, LIGHT, NAVY, ORANGE, PURPLE, apply_style, save


def to_bits(n: int, w: int = 4) -> list[int]:
    return [(n >> (w - 1 - i)) & 1 for i in range(w)]


def trace_rows():
    out = []
    for i in range(1, 9):
        before = to_bits(i - 1)
        after = to_bits(i)
        flipped = [b != a for b, a in zip(before, after)]
        t = sum(1 for b, a in zip(before, after) if b == 1 and a == 0)
        actual = t + 1
        phi_before, phi_after = sum(before), sum(after)
        dphi = phi_after - phi_before
        out.append({
            "i": i,
            "after": after,
            "flipped": flipped,
            "actual": actual,
            "dphi": dphi,
            "phi": phi_after,
            "amort": actual + dphi,
        })
    return out


def main() -> None:
    apply_style()
    rows = trace_rows()
    n = len(rows)

    fig = plt.figure(figsize=(6.6, 6.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.4, 1.0], hspace=0.28)

    # =======================================================================
    # TOP PANEL — table: row per step, columns for bits + actual + dPhi + amort
    # =======================================================================
    ax_t = fig.add_subplot(gs[0, 0])
    ax_t.axis("off")

    # Logical column layout: step | b3 b2 b1 b0 | actual | dPhi | amortized
    BIT_W = 0.92                 # width of a bit cell
    HEAD_X = 0.0                 # left edge of "step" column
    BITS_X0 = 1.20               # left edge of bit columns
    BITS_X1 = BITS_X0 + 4 * BIT_W
    GAP = 0.55
    COL_ACT = BITS_X1 + GAP + 0.10
    COL_DPHI = COL_ACT + 1.40
    COL_AMORT = COL_DPHI + 1.45
    RIGHT_EDGE = COL_AMORT + 1.55

    ROW_H = 0.66
    TOP_Y = (n + 1) * ROW_H      # y-coord of top of the header row
    ax_t.set_xlim(-0.30, RIGHT_EDGE + 0.20)
    ax_t.set_ylim(-0.40, TOP_Y + 1.35)

    # Header row -----------------------------------------------------------
    header_y = TOP_Y + ROW_H * 0.32
    ax_t.add_patch(Rectangle(
        (-0.20, TOP_Y - 0.10), RIGHT_EDGE + 0.30, ROW_H * 0.82,
        fc=LIGHT, ec="none",
    ))
    ax_t.text(HEAD_X + 0.55, header_y, "step",
              ha="center", va="center", fontsize=9.2, weight="bold", color=INK)
    ax_t.text(BITS_X0 + 2 * BIT_W, header_y + 0.16, "counter",
              ha="center", va="center", fontsize=9.2, weight="bold", color=INK)
    ax_t.text(BITS_X0 + 2 * BIT_W, header_y - 0.16,
              r"(MSB $\to$ LSB)",
              ha="center", va="center", fontsize=7.2, style="italic", color=GRAY)
    ax_t.text(COL_ACT, header_y, "actual",
              ha="center", va="center", fontsize=9.2, weight="bold", color=INK)
    ax_t.text(COL_DPHI, header_y, r"$\Delta\Phi$",
              ha="center", va="center", fontsize=10.0, weight="bold", color=PURPLE)
    ax_t.text(COL_AMORT, header_y, "amortized",
              ha="center", va="center", fontsize=9.2, weight="bold", color=NAVY)

    # separator line
    ax_t.plot([-0.20, RIGHT_EDGE + 0.10],
              [TOP_Y - 0.10, TOP_Y - 0.10], color=INK, lw=0.9)

    # Rows -----------------------------------------------------------------
    for j, r in enumerate(rows):
        y_top = TOP_Y - (j + 1) * ROW_H
        y_mid = y_top + ROW_H / 2
        # subtle banding
        if j % 2 == 1:
            ax_t.add_patch(Rectangle(
                (-0.20, y_top), RIGHT_EDGE + 0.30, ROW_H - 0.04,
                fc=to_rgba(NAVY, 0.05), ec="none",
            ))

        # step number
        ax_t.text(HEAD_X + 0.55, y_mid, str(r["i"]),
                  ha="center", va="center", fontsize=10, color=INK)

        # bit cells
        for b_idx, bit in enumerate(r["after"]):
            x0 = BITS_X0 + b_idx * BIT_W
            hot = r["flipped"][b_idx]
            fc = to_rgba(ORANGE, 0.24) if hot else (
                to_rgba(NAVY, 0.08) if bit else "white"
            )
            ax_t.add_patch(Rectangle(
                (x0 + 0.06, y_top + 0.06), BIT_W - 0.12, ROW_H - 0.12,
                fc=fc, ec=INK, lw=0.7,
            ))
            ax_t.text(x0 + BIT_W / 2, y_mid, str(bit),
                      ha="center", va="center",
                      fontsize=10.5,
                      color=ORANGE if hot else (NAVY if bit else INK),
                      weight="bold" if hot or bit else "normal",
                      family="monospace")

        # actual
        ax_t.text(COL_ACT, y_mid, str(r["actual"]),
                  ha="center", va="center", fontsize=10.5, color=INK)
        # dPhi
        sgn = "+" if r["dphi"] >= 0 else ""
        ax_t.text(COL_DPHI, y_mid, f"{sgn}{r['dphi']}",
                  ha="center", va="center", fontsize=10.5, color=PURPLE)
        # amortized (always 2 — emphasized)
        ax_t.text(COL_AMORT, y_mid, str(r["amort"]),
                  ha="center", va="center", fontsize=11,
                  color=NAVY, weight="bold")

    # right-hand totals strip
    tot_actual = sum(r["actual"] for r in rows)
    tot_amort = sum(r["amort"] for r in rows)
    foot_y = -0.20
    ax_t.plot([-0.20, RIGHT_EDGE + 0.10], [foot_y + 0.18, foot_y + 0.18],
              color=INK, lw=0.9)
    ax_t.text(HEAD_X + 0.55, foot_y, "total",
              ha="center", va="center", fontsize=9, style="italic", color=GRAY)
    ax_t.text(COL_ACT, foot_y, str(tot_actual),
              ha="center", va="center", fontsize=10, color=INK)
    ax_t.text(COL_DPHI, foot_y, f"{(tot_amort - tot_actual):+d}",
              ha="center", va="center", fontsize=10, color=PURPLE)
    ax_t.text(COL_AMORT, foot_y, f"{tot_amort} = 2n",
              ha="center", va="center", fontsize=10, color=NAVY, weight="bold")

    # legend for the highlight
    leg_y = TOP_Y + 1.05
    ax_t.add_patch(Rectangle((HEAD_X + 0.10, leg_y - 0.13),
                             0.26, 0.26,
                             fc=to_rgba(ORANGE, 0.24), ec=INK, lw=0.6))
    ax_t.text(HEAD_X + 0.45, leg_y, "= bit flipped on this step",
              ha="left", va="center",
              fontsize=8.0, style="italic", color=INK)

    # =======================================================================
    # BOTTOM PANEL — bars + lines
    # =======================================================================
    ax = fig.add_subplot(gs[1, 0])
    xs = [r["i"] for r in rows]
    actuals = [r["actual"] for r in rows]
    phis = [r["phi"] for r in rows]
    amorts = [r["amort"] for r in rows]

    ax.set_xlim(0.4, n + 0.6)
    ax.set_ylim(0.0, 5.2)
    ax.set_xticks(xs)
    ax.set_xlabel("increment $i$")
    ax.set_ylabel("cost / potential")
    ax.set_axisbelow(True)
    ax.grid(True, axis="y", color=LIGHT, lw=0.6)

    ax.bar(xs, actuals, width=0.62,
           color=to_rgba(ORANGE, 0.55), edgecolor=ORANGE, lw=0.8,
           zorder=2, label=r"actual cost $t+1$")
    ax.plot(xs, phis, color=PURPLE, lw=1.6, marker="o", markersize=4,
            label=r"potential $\Phi$ (# of 1-bits)", zorder=3)
    ax.plot(xs, amorts, color=NAVY, lw=1.8, marker="s", markersize=4.5,
            label="amortized $= 2$", zorder=4)

    ax.annotate(
        "carry chain $0111 \\to 1000$:\nactual $= 4$, $\\Delta\\Phi = -2$",
        xy=(8, 4.05), xytext=(5.6, 4.9),
        ha="left", va="top", fontsize=7.8, color=ORANGE,
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.9),
    )

    leg = ax.legend(loc="upper left", fontsize=7.8,
                    handlelength=1.4, handletextpad=0.5)
    for txt in leg.get_texts():
        txt.set_color(INK)

    fig.subplots_adjust(top=0.95, bottom=0.10, left=0.10, right=0.97)
    fig.text(0.5, 0.02,
             r"each expensive step is paid for by the potential it crashes:"
             r" actual $+\,\Delta\Phi = (t+1)+(1-t) = 2$",
             ha="center", va="bottom", fontsize=8.5, style="italic", color=INK)

    save(fig, "binary-counter-amortized-trace")


if __name__ == "__main__":
    main()
