"""adaptive_engine: the computational core of CogniPlay's adaptive difficulty system.

This package implements the "Adaptive Algorithm Service" described in the
CogniPlay architecture (Assignment 2): an Item-Response-Theory (IRT) based
engine that estimates a user's cognitive ability in near real time and
selects the next exercise at the difficulty level that is most informative
for that estimate, plus a thin gamification layer that converts session
performance into points.

Modules:
    irt            -- 2-parameter logistic (2PL) IRT model: response
                       probability, Fisher information, online ability update
    item_bank      -- exercise item representation and loading
    selector       -- next-item selection via maximum Fisher information
    gamification   -- XP / streak scoring for the gamification layer
    simulate       -- end-to-end adaptive-session simulator
    plotting       -- convergence / item-bank plots (headless matplotlib)
    cli            -- command-line interface
"""

__version__ = "0.1.0"
