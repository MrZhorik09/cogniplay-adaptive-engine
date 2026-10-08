"""Next-item selection for computerized adaptive testing (CAT).

The strategy implemented here is the classic *maximum information*
criterion: among the items not yet administered in the current session,
pick the one whose Fisher information is highest at the user's current
ability estimate. This concentrates exercises around the difficulty level
where the user's true ability is most precisely resolved, which is exactly
the "continuously recalibrates exercise difficulty ... in near real time"
behavior described for CogniPlay's adaptive engine in Assignment 2.
"""

from __future__ import annotations

from .irt import fisher_information
from .item_bank import Item


def select_next_item(theta: float, items: list[Item], administered_ids: set[str]) -> Item:
    """Return the available item with maximum Fisher information at ``theta``.

    Raises
    ------
    ValueError
        If every item in ``items`` has already been administered.
    """
    candidates = [item for item in items if item.item_id not in administered_ids]
    if not candidates:
        raise ValueError("No remaining items to administer: the item bank is exhausted")

    return max(candidates, key=lambda item: fisher_information(theta, item.a, item.b))
