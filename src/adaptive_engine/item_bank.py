"""Representation and loading of the cognitive-exercise item bank.

Each row of the item bank corresponds to one exercise template in CogniPlay
(e.g., a specific working-memory span task configuration), described by its
cognitive domain and its 2PL item parameters.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

VALID_DOMAINS = {"memory", "attention", "speed", "reasoning"}


@dataclass(frozen=True)
class Item:
    """A single exercise item with its IRT parameters."""

    item_id: str
    domain: str
    a: float  # discrimination
    b: float  # difficulty

    def __post_init__(self):
        if self.domain not in VALID_DOMAINS:
            raise ValueError(f"Unknown domain '{self.domain}', expected one of {VALID_DOMAINS}")
        if self.a <= 0:
            raise ValueError("Discrimination 'a' must be positive")


def load_item_bank(path: str) -> list[Item]:
    """Load an item bank from a CSV file with columns:
    item_id, domain, a, b.
    """
    df = pd.read_csv(path)
    required = {"item_id", "domain", "a", "b"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Item bank is missing required columns: {sorted(missing)}")

    return [
        Item(item_id=str(row.item_id), domain=str(row.domain),
             a=float(row.a), b=float(row.b))
        for row in df.itertuples(index=False)
    ]


def item_bank_to_dataframe(items: list[Item]) -> pd.DataFrame:
    """Convert a list of Items back into a DataFrame (useful for plotting)."""
    return pd.DataFrame(
        [{"item_id": i.item_id, "domain": i.domain, "a": i.a, "b": i.b} for i in items])
