"""Command-line interface for the CogniPlay adaptive engine.

Examples
--------
Run an adaptive session simulation and print a summary::

    python -m adaptive_engine.cli simulate --items data/sample_item_bank.csv \\
        --true-theta 1.2 --rounds 25 --seed 7

Also save a convergence plot::

    python -m adaptive_engine.cli simulate --items data/sample_item_bank.csv \\
        --true-theta 1.2 --rounds 25 --seed 7 --plot docs/convergence.png

Plot the item bank itself::

    python -m adaptive_engine.cli item-bank-plot --items data/sample_item_bank.csv \\
        --output docs/item_bank.png
"""

from __future__ import annotations

import argparse
import json
import sys

from .item_bank import item_bank_to_dataframe, load_item_bank
from .plotting import plot_convergence, plot_item_bank
from .simulate import simulate_session


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adaptive_engine", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    sim_parser = subparsers.add_parser(
        "simulate", help="Simulate an adaptive training session for a synthetic user")
    sim_parser.add_argument("--items", required=True, help="Path to the item bank CSV")
    sim_parser.add_argument(
        "--true-theta", type=float, required=True, help="The synthetic user's true ability")
    sim_parser.add_argument(
        "--rounds", type=int, required=True, help="Number of items to administer")
    sim_parser.add_argument(
        "--initial-theta", type=float, default=0.0,
        help="Starting ability estimate (default: 0.0)")
    sim_parser.add_argument("--seed", type=int, default=None, help="Random seed")
    sim_parser.add_argument(
        "--plot", default=None, help="Optional path to save a convergence plot")

    bank_parser = subparsers.add_parser(
        "item-bank-plot", help="Plot the difficulty/discrimination spread of an item bank")
    bank_parser.add_argument("--items", required=True, help="Path to the item bank CSV")
    bank_parser.add_argument("--output", required=True, help="Output image path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "simulate":
        items = load_item_bank(args.items)
        result = simulate_session(
            items, true_theta=args.true_theta, rounds=args.rounds,
            initial_theta=args.initial_theta, seed=args.seed)
        summary = {
            "rounds": args.rounds,
            "true_theta": result.true_theta,
            "final_theta_estimate": result.final_theta,
            "final_error": result.final_error,
            "total_xp": result.total_xp,
            "best_streak": result.best_streak,
        }
        print(json.dumps(summary, indent=2))
        if args.plot:
            path = plot_convergence(result, args.plot)
            print(f"Saved convergence plot to {path}")
        return 0

    if args.command == "item-bank-plot":
        items = load_item_bank(args.items)
        df = item_bank_to_dataframe(items)
        path = plot_item_bank(df, args.output)
        print(f"Saved item bank plot to {path}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
