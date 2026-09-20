"""Rebuild the three locked R6R8 manuscript figures from admitted CSV values."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def style() -> None:
    plt.rcParams.update({
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "figure.dpi": 150,
        "savefig.bbox": "tight",
    })


def rank_vs_loss(data: pd.DataFrame, output: Path) -> None:
    fig, axis = plt.subplots(figsize=(7.2, 4.2))
    for family, marker in (("Norway", "o"), ("Boulder >=30 d", "s")):
        frame = data[data["family"] == family]
        axis.scatter(frame["same_budget_percentile_pct"], frame["transferred_loss_pct"], marker=marker, s=28, label=family)
    axis.axhline(5.0, linestyle="--", linewidth=1.0, label="5% descriptive read-off")
    axis.set(xlabel=r"Exact same-budget percentile at $k=4$ (%)", ylabel=r"Transferred Pareto loss at $k=4$ (%)", xlim=(75, 100.5), ylim=(0, 46))
    axis.set_title("High relative rank can coexist with poor absolute coverage")
    axis.grid(True, alpha=0.3)
    axis.legend(loc="upper left")
    point = data[data["target"] == "BOULDER PARK S1"].iloc[0]
    axis.annotate("BOULDER PARK S1\n99.66% rank, 16.809% loss", xy=(point.same_budget_percentile_pct, point.transferred_loss_pct), xytext=(93.2, 23.5), arrowprops={"arrowstyle": "-", "lw": 0.9}, fontsize=7)
    fig.savefig(output)
    plt.close(fig)


def family_bars(summary: pd.DataFrame, output: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.7, 3.7))
    families = ["Norway", "Boulder >=30 d"]
    for axis, grid in zip(axes, ("3x3", "5x5")):
        frame = summary[summary["grid"] == grid].set_index("family").loc[families]
        x = np.arange(2)
        width = 0.36
        axis.bar(x - width / 2, frame["median_local_floor_pct"], width, label="Target-local floor")
        axis.bar(x + width / 2, frame["median_transferred_loss_pct"], width, label="Transferred loss")
        axis.set_xticks(x, families)
        axis.set_title(rf"{grid[0]}$\times${grid[-1]} candidate lattice")
        axis.set_ylabel("Median target Pareto loss (%)")
        axis.grid(True, axis="y", alpha=0.3)
        for position, value in enumerate(frame["median_selection_excess_pp"]):
            axis.text(position, frame.iloc[position]["median_transferred_loss_pct"] + 0.04 * axis.get_ylim()[1], rf"med. $\Delta^{{sel}}$={value:.3g} pp", ha="center", fontsize=7)
    axes[0].legend(loc="upper left")
    fig.suptitle("Target-local floor and transferred-selection loss are distinct components")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)


def decomposition(data: pd.DataFrame, output: Path) -> None:
    fig, axis = plt.subplots(figsize=(7.2, 4.5))
    for family, marker in (("Norway", "o"), ("Boulder >=30 d", "s")):
        frame = data[data["family"] == family]
        axis.scatter(frame["local_floor_pct"], frame["selection_excess_pp"], marker=marker, s=28, label=family)
    x = np.linspace(0, 5, 100)
    axis.plot(x, 5 - x, linestyle="--", linewidth=1.0, label=r"$\varepsilon^{dev}=5\%$ reference")
    axis.axvline(5.0, linestyle=":", linewidth=1.2, label=r"$\varepsilon^{loc}=5\%$ reference")
    axis.set(xlabel=r"Best attainable target-local loss at current budget, $\varepsilon^{loc}$ (%)", ylabel=r"Transfer-selection excess, $\Delta^{sel}$ (percentage points)", xlim=(0, 22), ylim=(0, 31.5))
    axis.set_title("Target-level decomposition of transferred portfolio loss")
    axis.grid(True, alpha=0.3)
    axis.legend(loc="upper right")
    point = data[data["target"] == "BOULDER PARK S1"].iloc[0]
    axis.annotate(r"BOULDER PARK S1" + "\n" + r"$\varepsilon^{loc}$=7.387%, $\Delta^{sel}$=9.422 pp", xy=(point.local_floor_pct, point.selection_excess_pp), xytext=(10.0, 16.8), arrowprops={"arrowstyle": "-", "lw": 0.9}, fontsize=7)
    fig.savefig(output)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).parents[1] / "reproducibility" / "reference" / "derived")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    style()
    data = pd.read_csv(args.data_dir / "target_decomposition_values.csv")
    summary = pd.read_csv(args.data_dir / "family_resolution_summary.csv")
    rank_vs_loss(data, args.output_dir / "fig2_rank_vs_loss.pdf")
    family_bars(summary, args.output_dir / "fig3_decomposition.pdf")
    decomposition(data, args.output_dir / "fig1_target_decomposition.pdf")


if __name__ == "__main__":
    main()
