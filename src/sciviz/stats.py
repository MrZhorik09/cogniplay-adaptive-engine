"""Descriptive statistics helpers for experimental / scientific datasets."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd


@dataclass
class DescriptiveStats:
    """Container for descriptive statistics of a single numeric sample."""

    n: int
    mean: float
    std: float
    minimum: float
    maximum: float
    median: float
    ci95_low: float
    ci95_high: float

    def as_dict(self) -> dict:
        return {
            "n": self.n,
            "mean": self.mean,
            "std": self.std,
            "min": self.minimum,
            "max": self.maximum,
            "median": self.median,
            "ci95_low": self.ci95_low,
            "ci95_high": self.ci95_high,
        }


def load_dataset(path: str) -> pd.DataFrame:
    """Load a CSV dataset into a pandas DataFrame.

    Parameters
    ----------
    path:
        Path to a CSV file. The first row must contain column headers.

    Returns
    -------
    pandas.DataFrame
    """
    return pd.read_csv(path)


def confidence_interval_95(mean: float, std: float, n: int) -> tuple[float, float]:
    """Compute an approximate 95% confidence interval for the mean.

    Uses the normal approximation (z = 1.96), which is appropriate for the
    moderate-to-large sample sizes typical of exported experiment logs.
    """
    if n <= 1 or std == 0:
        return (mean, mean)
    margin = 1.96 * (std / math.sqrt(n))
    return (mean - margin, mean + margin)


def descriptive_stats(df: pd.DataFrame, column: str) -> DescriptiveStats:
    """Compute descriptive statistics for a numeric column.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``df``.
    ValueError
        If the column contains no numeric data after dropping NaNs.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in dataset")

    series = pd.to_numeric(df[column], errors="coerce").dropna()
    if series.empty:
        raise ValueError(f"Column '{column}' has no numeric values")

    n = int(series.count())
    mean = float(series.mean())
    std = float(series.std(ddof=1)) if n > 1 else 0.0
    ci_low, ci_high = confidence_interval_95(mean, std, n)

    return DescriptiveStats(
        n=n,
        mean=mean,
        std=std,
        minimum=float(series.min()),
        maximum=float(series.max()),
        median=float(series.median()),
        ci95_low=ci_low,
        ci95_high=ci_high,
    )
