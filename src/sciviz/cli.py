"""Command-line interface for sciviz.

Examples
--------
Compute descriptive statistics for a column::

    python -m sciviz.cli stats data/sample_experiment.csv --column measurement

Create a histogram::

    python -m sciviz.cli plot data/sample_experiment.csv --kind histogram \\
        --column measurement --output histogram.png

Create a scatter plot::

    python -m sciviz.cli plot data/sample_experiment.csv --kind scatter \\
        --x time_s --y measurement --output scatter.png
"""

from __future__ import annotations

import argparse
import json
import sys

from .plotting import plot_histogram, plot_line_with_error, plot_scatter
from .stats import descriptive_stats, load_dataset


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sciviz", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    stats_parser = subparsers.add_parser(
        "stats", help="Compute descriptive statistics for a column")
    stats_parser.add_argument("csv_path", help="Path to the input CSV file")
    stats_parser.add_argument("--column", required=True, help="Name of the numeric column")

    plot_parser = subparsers.add_parser("plot", help="Generate a plot from a CSV file")
    plot_parser.add_argument("csv_path", help="Path to the input CSV file")
    plot_parser.add_argument("--kind", choices=["histogram", "scatter", "line"], required=True)
    plot_parser.add_argument("--column", help="Column name (for histogram)")
    plot_parser.add_argument("--x", help="X-axis column (for scatter/line)")
    plot_parser.add_argument("--y", help="Y-axis column (for scatter/line)")
    plot_parser.add_argument("--yerr", help="Column with y error values (for line)")
    plot_parser.add_argument("--output", required=True, help="Output image path (e.g. plot.png)")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    df = load_dataset(args.csv_path)

    if args.command == "stats":
        result = descriptive_stats(df, args.column)
        print(json.dumps(result.as_dict(), indent=2))
        return 0

    if args.command == "plot":
        if args.kind == "histogram":
            if not args.column:
                parser.error("--column is required for --kind histogram")
            path = plot_histogram(df, args.column, args.output)
        elif args.kind == "scatter":
            if not (args.x and args.y):
                parser.error("--x and --y are required for --kind scatter")
            path = plot_scatter(df, args.x, args.y, args.output)
        else:  # line
            if not (args.x and args.y and args.yerr):
                parser.error("--x, --y and --yerr are required for --kind line")
            path = plot_line_with_error(df, args.x, args.y, args.yerr, args.output)
        print(f"Saved plot to {path}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
