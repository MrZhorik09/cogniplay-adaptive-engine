"""End-to-end simulation of one adaptive CogniPlay training session.

Ties together item selection (selector.py), ability updating (irt.py) and
scoring (gamification.py) into the same loop that would run, item by item,
inside the real Adaptive Algorithm Service: pick the most informative item
for the user's current estimated ability, simulate (or, in production,
observe) their response, update the ability estimate, award XP, repeat.

Because a user's *true* ability is never directly observable, this module
models it explicitly (``true_theta``) so the simulation can report how
quickly and accurately the online estimate converges toward it -- a useful
sanity check on the algorithm, analogous to the pilot-cohort validation
recommended in Assignment 2 (risk R1).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from .gamification import SessionScorer
from .irt import probability_correct, update_ability
from .item_bank import Item
from .selector import select_next_item


@dataclass
class SimulationResult:
    true_theta: float
    theta_history: list = field(default_factory=list)  # length == rounds + 1 (includes initial)
    total_xp: int = 0
    best_streak: int = 0
    records: list = field(default_factory=list)

    @property
    def final_theta(self) -> float:
        return self.theta_history[-1]

    @property
    def final_error(self) -> float:
        """Absolute error between the final ability estimate and the true ability."""
        return abs(self.final_theta - self.true_theta)


def simulate_session(
    items: list[Item], true_theta: float, rounds: int,
    initial_theta: float = 0.0, seed: int | None = None,
) -> SimulationResult:
    """Simulate ``rounds`` adaptively-selected items for a synthetic user.

    Parameters
    ----------
    items:
        The available item bank.
    true_theta:
        The synthetic user's true (latent) ability, used only to generate
        simulated responses -- the algorithm itself never sees this value.
    rounds:
        Number of items to administer.
    initial_theta:
        Starting ability estimate before any items are seen (CogniPlay would
        typically start new users at 0.0, i.e. "average").
    seed:
        Optional random seed for reproducibility.
    """
    if rounds < 1:
        raise ValueError("rounds must be >= 1")
    if rounds > len(items):
        raise ValueError(f"rounds ({rounds}) cannot exceed the item bank size ({len(items)})")

    rng = random.Random(seed)
    theta_est = initial_theta
    administered: set = set()
    scorer = SessionScorer()
    theta_history = [theta_est]

    for round_number in range(1, rounds + 1):
        item = select_next_item(theta_est, items, administered)
        administered.add(item.item_id)

        p_true = probability_correct(true_theta, item.a, item.b)
        correct = rng.random() < p_true

        scorer.record(item, correct)
        theta_est = update_ability(theta_est, item.a, item.b, correct, n_attempts=round_number)
        theta_history.append(theta_est)

    return SimulationResult(
        true_theta=true_theta,
        theta_history=theta_history,
        total_xp=scorer.total_xp,
        best_streak=scorer.best_streak,
        records=scorer.history,
    )
