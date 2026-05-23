import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FixedLocator, FuncFormatter
import pandas as pd
import sys


def _select_biolinum_font():
    preferred_fonts = ["Linux Biolinum O", "Linux Biolinum"]
    available_fonts = {font.name for font in font_manager.fontManager.ttflist}

    for font_name in preferred_fonts:
        if font_name in available_fonts:
            return font_name

    print(
        'Error: neither "Linux Biolinum O" nor "Linux Biolinum" is available.',
        file=sys.stderr,
    )
    sys.exit(1)


def plot_iteration_time(df, output_path, bench):
    """
    Plots the iteration time, i.e., the `value` column, for a specific benchmark.

    The x-axis is the iteration number and the y-axis is `value`.
    Data points are grouped by `invocation` so each invocation is shown as
    a separate series.
    The `unit` column is used to label the y-axis.
    """
    required_columns = ["bench", "invocation", "iteration", "unit", "value"]
    plot_df = df.loc[df["bench"] == bench, required_columns].copy()
    if plot_df.empty:
        raise ValueError(f"No rows found for bench '{bench}'")

    plot_df["iteration"] = pd.to_numeric(plot_df["iteration"], errors="coerce")
    plot_df["value"] = pd.to_numeric(plot_df["value"], errors="coerce")
    plot_df = plot_df.dropna(subset=["invocation", "iteration", "value", "unit"])
    if plot_df.empty:
        raise ValueError(f"No plottable rows for bench '{bench}' after filtering")

    units = sorted(plot_df["unit"].astype(str).unique())
    unit_label = units[0] if len(units) == 1 else ", ".join(units)

    selected_font = _select_biolinum_font()
    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": [selected_font, "sans-serif"],
        }
    )

    invocations = sorted(plot_df["invocation"].unique())
    fig, ax = plt.subplots(figsize=(5, 2.8))

    for invocation in invocations:
        invocation_df = plot_df.loc[plot_df["invocation"] == invocation].sort_values(
            by="iteration"
        )
        ax.plot(
            invocation_df["iteration"],
            invocation_df["value"],
            linestyle="None",
            marker="o",
            markersize=1,
            alpha=0.25,
            label=f"invocation {invocation}",
        )

    ax.set_title(bench)
    ax.set_xlabel("iteration")
    ax.set_ylabel(f"run time in {unit_label}")
    ax.set_ylim(bottom=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if len(invocations) <= 8:
        ax.legend(frameon=False, fontsize=8)

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved iteration-time plot to: {output_path}")


def plot_change(change_df, output_path):
    plot_df = change_df.copy()
    plot_df = plot_df.dropna(subset=["bench", "unit", "normalized_value"])

    bench_order = sorted(plot_df["bench"].unique())
    plot_df["bench"] = pd.Categorical(
        plot_df["bench"], categories=bench_order, ordered=True
    )

    selected_font = _select_biolinum_font()

    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": [selected_font, "sans-serif"],
        }
    )
    fig, ax = plt.subplots(figsize=(5, max(2, int(len(bench_order) * 0.23))))
    plot_df.boxplot(
        column="normalized_value",
        by="bench",
        vert=False,
        ax=ax,
        patch_artist=True,
        boxprops={"facecolor": "#729fcf", "edgecolor": "#729fcf"},
        medianprops={"color": "black", "linewidth": 1.25},
        flierprops={"markersize": 2, "alpha": 0.1},
    )

    fig.suptitle("")
    ax.set_title("")
    ax.set_xlabel(f"run time factor compared to baseline")
    ax.set_ylabel("")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.set_xscale("log")
    ax.set_xlim(0.1, 10)

    tick_formatter = FuncFormatter(lambda x, _: f"{x:g}")
    ax.xaxis.set_major_formatter(tick_formatter)
    ax.xaxis.set_minor_locator(FixedLocator([0.5, 2]))
    ax.xaxis.set_minor_formatter(
        FuncFormatter(lambda x, _: f"{x:g}" if x in (0.5, 2) else "")
    )

    ax.tick_params(axis="x", which="both", length=4, width=1)

    ax.axvline(1, linestyle=":", color="black", linewidth=1)
    ax.invert_yaxis()  # alphabetical, from the top instead of from 0,0
    plt.tight_layout()

    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved box plot to: {output_path}")
