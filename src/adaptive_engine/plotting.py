"""Plotting helpers for the adaptive engine, using a non-interactive
matplotlib backend so they also run headless inside CI."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # must happen before pyplot import, enables headless CI runs

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .simulate import SimulationResult  # noqa: E402


def plot_convergence(
    result: SimulationResult, output_path: str, title: str | None = None,
) -> str:
    """Plot the estimated-ability trajectory against the true ability.

    Visualizes how quickly the online IRT ability estimate (Section
    irt.update_ability) converges toward the synthetic user's true ability
    over the course of a simulated session.
    """
    rounds = list(range(len(result.theta_history)))

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(rounds, result.theta_history, color="#2f6fa8", marker="o", markersize=3,
            linewidth=1.5, label="Estimated ability (theta)")
    ax.axhline(result.true_theta, color="#b8860b", linestyle="--", linewidth=1.5,
               label=f"True ability ({result.true_theta:.2f})")
    ax.set_xlabel("Round (items administered)")
    ax.set_ylabel("Ability estimate (theta)")
    ax.set_title(title or "Convergence of the adaptive ability estimate")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_item_bank(df: pd.DataFrame, output_path: str, title: str | None = None) -> str:
    """Scatter plot of the item bank: difficulty (b) vs. discrimination (a),
    colored by cognitive domain."""
    fig, ax = plt.subplots(figsize=(6.5, 4))
    domains = sorted(df["domain"].unique())
    colors = plt.get_cmap("tab10").colors
    for i, domain in enumerate(domains):
        subset = df[df["domain"] == domain]
        ax.scatter(subset["b"], subset["a"], label=domain, alpha=0.8,
                   color=colors[i % len(colors)], edgecolor="white")
    ax.set_xlabel("Difficulty (b)")
    ax.set_ylabel("Discrimination (a)")
    ax.set_title(title or "Item bank: difficulty vs. discrimination")
    ax.legend(title="Domain")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
