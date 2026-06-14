"""Memory-hierarchy access latencies on a log scale (§28.2): the staircase the RAM model flattens to cost 1."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt

from _style import GRAY, INK, ORANGE, apply_style, save

# (level, latency in ns) — from the table in §28.2.
LEVELS = [
    ("Register", 0.5),
    ("L1 cache", 1.0),
    ("L2 cache", 4.0),
    ("L3 cache", 12.0),
    ("Main memory", 100.0),
    ("SSD", 1e5),
    ("Spinning disk", 1e7),
]

LEFT = 0.3  # left edge of bars / x-axis (log scale cannot start at 0)


def fmt_latency(ns: float) -> str:
    """Human-readable latency, matching the document's table."""
    if ns < 1:
        return "< 1 ns"
    if ns < 1e3:
        return f"{ns:g} ns"
    if ns < 1e6:
        return f"{ns / 1e3:g} µs"
    return f"{ns / 1e6:g} ms"


def fmt_human(ns: float) -> str:
    """Latency rescaled so 1 ns = 1 s."""
    s = ns  # nanoseconds -> seconds under the rescaling
    if s < 1:
        return "< 1 s"
    if s < 60:
        return f"{s:g} s"
    if s < 3600:
        return f"~{round(s / 60):g} min"
    if s < 30 * 86400:
        return f"~{round(s / 3600):g} h"
    return f"~{round(s / (30 * 86400)):g} months"


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(6.0, 3.1))

    names = [name for name, _ in LEVELS]
    lats = [lat for _, lat in LEVELS]
    ys = list(range(len(LEVELS) - 1, -1, -1))  # Register on top

    ax.barh(
        ys,
        [lat - LEFT for lat in lats],
        left=LEFT,
        height=0.62,
        color=GRAY,
        edgecolor=INK,
        linewidth=0.7,
        zorder=3,
    )

    # Latency label at the right end of each bar.
    for y, lat in zip(ys, lats):
        ax.text(
            lat * 1.35,
            y,
            fmt_latency(lat),
            va="center",
            ha="left",
            fontsize=8.5,
            color=INK,
            fontweight="bold",
            zorder=4,
        )

    # Far-right column: latencies rescaled to human time (1 ns = 1 s).
    trans = ax.get_yaxis_transform()  # x in axes fraction, y in data coords
    ax.text(
        1.035,
        len(LEVELS) - 0.35,
        "human scale\n(1 ns = 1 s)",
        transform=trans,
        ha="left",
        va="bottom",
        fontsize=8,
        style="italic",
        color=INK,
    )
    for y, lat in zip(ys, lats):
        ax.text(
            1.035,
            y,
            fmt_human(lat),
            transform=trans,
            ha="left",
            va="center",
            fontsize=8.5,
            color=INK,
        )

    # Bracket across the gap between Main memory (100 ns) and SSD (100 us).
    y_main, y_ssd = ys[4], ys[5]
    y_br = (y_main + y_ssd) / 2  # midline between the two rows
    ram_lat, ssd_lat = lats[4], lats[5]
    ax.annotate(
        "",
        xy=(ssd_lat, y_br),
        xytext=(ram_lat, y_br),
        arrowprops=dict(arrowstyle="|-|,widthA=0.25,widthB=0.25", color=ORANGE, lw=1.3),
        zorder=4,
    )
    ax.text(
        (ram_lat * ssd_lat) ** 0.5,  # geometric midpoint on the log axis
        y_br,
        "$1000\\times$ cliff: leaving RAM",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=ORANGE,
        zorder=4,
        bbox=dict(facecolor="white", edgecolor="none", pad=1.2),
    )

    # The one-line moral, placed in the empty upper-right region.
    ax.text(
        0.98,
        0.94,
        "The RAM model charges every one of these the same: cost 1.",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        style="italic",
        color=INK,
    )

    ax.set_xscale("log")
    ax.set_xlim(LEFT, 1e8)
    ax.set_ylim(-0.55, len(LEVELS) - 0.45)
    ax.set_yticks(ys)
    ax.set_yticklabels(names)
    decades = [10.0**k for k in range(8)]
    ax.set_xticks(decades)
    ax.set_xticklabels(
        ["1 ns", "10 ns", "100 ns", "1 µs", "10 µs", "100 µs", "1 ms", "10 ms"]
    )
    ax.set_xticks([], minor=True)
    ax.set_xlabel("access latency (log scale — each gridline is $10\\times$ slower)")
    ax.grid(axis="x", which="major", color="#d4d4dd", zorder=0)
    ax.tick_params(axis="y", length=0)

    save(fig, "memory-hierarchy-latency-logscale")


if __name__ == "__main__":
    main()
