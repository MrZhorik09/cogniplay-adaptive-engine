"""Plotting helpers built on matplotlib, using a non-interactive backend
so they can run headless in CI."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # must happen before pyplot import, enables headless CI runs

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def plot_histogram(
    df: pd.DataFrame, column: str, output_path: str, bins: int = 20,
    title: str | None = None,
) -> str:
    """Save a histogram of ``column`` to ``output_path`` and return the path."""
    values = pd.to_numeric(df[column], errors="coerce").dropna()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(values, bins=bins, color="#2f6fa8", edgecolor="white")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    ax.set_title(title or f"Distribution of {column}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_scatter(
    df: pd.DataFrame, x: str, y: str, output_path: str,
    with_trendline: bool = True, title: str | None = None,
) -> str:
    """Save a scatter plot of ``y`` vs ``x`` with an optional linear trendline."""
    xs = pd.to_numeric(df[x], errors="coerce")
    ys = pd.to_numeric(df[y], errors="coerce")
    mask = xs.notna() & ys.notna()
    xs, ys = xs[mask], ys[mask]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(xs, ys, color="#2f6fa8", alpha=0.7, edgecolor="white")

    if with_trendline and len(xs) >= 2:
        coeffs = np.polyfit(xs, ys, 1)
        trend_x = np.linspace(xs.min(), xs.max(), 100)
        trend_y = np.polyval(coeffs, trend_x)
        ax.plot(trend_x, trend_y, color="#b8860b", linewidth=2,
                label=f"fit: y={coeffs[0]:.3g}x+{coeffs[1]:.3g}")
        ax.legend()

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title or f"{y} vs {x}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_line_with_error(
    df: pd.DataFrame, x: str, y: str, yerr: str, output_path: str,
    title: str | None = None,
) -> str:
    """Save a line plot of ``y`` vs ``x`` with vertical error bars from ``yerr``."""
    data = df[[x, y, yerr]].apply(pd.to_numeric, errors="coerce").dropna()
    data = data.sort_values(by=x)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(data[x], data[y], yerr=data[yerr], fmt="-o", color="#2f6fa8",
                ecolor="#b8860b", capsize=3)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title or f"{y} vs {x} (with error bars)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
