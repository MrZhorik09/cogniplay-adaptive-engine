"""Gamification scoring layer.

Converts the outcome of each exercise attempt into experience points (XP),
with a bonus for harder items and for answer streaks. This is a deliberately
small stand-in for CogniPlay's full Gamification Engine (Assignment 2),
focused on the one rule that actually depends on the adaptive algorithm's
output: harder, well-targeted items should be worth more than easy ones.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .item_bank import Item

BASE_XP = 10
CONSOLATION_XP = 2
STREAK_BONUS_PER_STEP = 5
STREAK_BONUS_THRESHOLD = 2  # streak bonus starts kicking in after this many in a row


def compute_xp(item: Item, correct: bool, streak_after: int) -> int:
    """Compute the XP awarded for one answered item.

    Parameters
    ----------
    item:
        The item that was just answered.
    correct:
        Whether the answer was correct.
    streak_after:
        The user's consecutive-correct streak *after* this answer (0 if the
        answer was incorrect).
    """
    if not correct:
        return CONSOLATION_XP

    difficulty_bonus = max(0.0, item.b) * 5.0
    streak_bonus = STREAK_BONUS_PER_STEP * max(0, streak_after - STREAK_BONUS_THRESHOLD)
    return round(BASE_XP + difficulty_bonus + streak_bonus)


@dataclass
class SessionScorer:
    """Stateful wrapper that tracks streaks and accumulated XP across a session."""

    streak: int = 0
    best_streak: int = 0
    total_xp: int = 0
    history: list = field(default_factory=list)

    def record(self, item: Item, correct: bool) -> int:
        """Record one answer, update streak/XP state, and return the XP awarded."""
        self.streak = self.streak + 1 if correct else 0
        self.best_streak = max(self.best_streak, self.streak)
        xp = compute_xp(item, correct, self.streak)
        self.total_xp += xp
        self.history.append(
            {"item_id": item.item_id, "correct": correct, "xp": xp, "streak": self.streak})
        return xp
