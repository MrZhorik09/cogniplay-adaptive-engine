"""2-parameter logistic (2PL) Item Response Theory model.

The 2PL model expresses the probability that a user with ability ``theta``
answers an item correctly as a logistic function of the gap between their
ability and the item's difficulty, scaled by the item's discrimination:

    P(correct | theta, a, b) = 1 / (1 + exp(-a * (theta - b)))

where:
    theta -- the user's latent ability (unbounded real number; 0 is "average")
    b     -- item difficulty (the ability level at which P = 0.5)
    a     -- item discrimination (how sharply P changes around theta == b)

This is the standard model used in computerized adaptive testing (CAT) and
is a reasonable, well-understood basis for CogniPlay's adaptive difficulty
engine: it lets every exercise be described by two interpretable numbers
and gives a principled way to estimate, and continuously update, how a
given user is doing.
"""

from __future__ import annotations

import math


def probability_correct(theta: float, a: float, b: float) -> float:
    """Return P(correct) under the 2PL model for ability ``theta`` and
    item parameters ``a`` (discrimination) and ``b`` (difficulty)."""
    z = a * (theta - b)
    # Numerically stable logistic function.
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    ez = math.exp(z)
    return ez / (1.0 + ez)


def fisher_information(theta: float, a: float, b: float) -> float:
    """Return the Fisher information of an item at ability ``theta``.

    Under the 2PL model, I(theta) = a^2 * P * (1 - P). Items are most
    informative (and therefore most useful to administer) near their own
    difficulty, where P is close to 0.5.
    """
    p = probability_correct(theta, a, b)
    return (a ** 2) * p * (1.0 - p)


def update_ability(
    theta: float, a: float, b: float, correct: bool, n_attempts: int,
    base_rate: float = 0.5,
) -> float:
    """Update the ability estimate after one observed response.

    This uses a simplified online update (a single step of gradient ascent
    on the item's log-likelihood, in the spirit of Elo-style rating
    systems): the estimate moves toward the outcome actually observed, by
    an amount proportional to the surprise (observed - predicted) and to
    the item's discrimination. The step size shrinks as ``n_attempts``
    grows, which stabilizes the estimate over a session instead of letting
    it oscillate indefinitely -- a practical trade-off against a full
    maximum-likelihood re-fit over the entire response history, which
    would be more accurate but is unnecessary for real-time adaptation
    within a single training session.

    Parameters
    ----------
    theta:
        Current ability estimate.
    a, b:
        Discrimination and difficulty of the item just answered.
    correct:
        Whether the response was correct.
    n_attempts:
        Number of items answered so far in the session, *including* this
        one (used to shrink the learning rate over time).
    base_rate:
        Base learning-rate constant; larger values adapt faster but are
        noisier.
    """
    if n_attempts < 1:
        raise ValueError("n_attempts must be >= 1")

    predicted = probability_correct(theta, a, b)
    observed = 1.0 if correct else 0.0
    learning_rate = base_rate / math.sqrt(n_attempts)
    return theta + learning_rate * a * (observed - predicted)
