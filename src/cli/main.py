#!/usr/bin/env python3
"""
CLI client for Pokemon Unite Meta Analysis API
"""

import argparse
import logging
import re
import sys
from typing import Any, Dict, Optional

import httpx
import pandas as pd

API_BASE_URL = "http://localhost:8000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pokemon_unite_cli")

# Suppress httpx INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)


def get_health() -> None:
    """Check API health endpoint."""
    try:
        response = httpx.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        print("API Health:", response.json())
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        sys.exit(1)


def colorize_role(text: str) -> str:
    """Apply color to lines based on role keywords."""
    text = re.sub(
        r"(.*Support.*)", r"\033[38;5;214m\1\033[0m", text, flags=re.IGNORECASE
    )
    text = re.sub(
        r"(.*Attacker.*)", r"\033[38;5;1m\1\033[0m", text, flags=re.IGNORECASE
    )
    text = re.sub(
        r"(.*Speedster.*)", r"\033[38;5;4m\1\033[0m", text, flags=re.IGNORECASE
    )
    text = re.sub(
        r"(.*Defender.*)", r"\033[1;38;5;2m\1\033[0m", text, flags=re.IGNORECASE
    )
    text = re.sub(
        r"(.*All-Rounder.*)",
        r"\033[38;5;93m\1\033[0m",
        text,
        flags=re.IGNORECASE,
    )
    return text


def get_builds(
    params: Optional[Dict[str, Any]] = None,
    include: Optional[list] = None,
    exclude: Optional[list] = None,
) -> None:
    """
    Fetch builds from the API with optional query params and print colorized
    output using pandas DataFrame. Allows column selection.
    """
    try:
        response = httpx.get(f"{API_BASE_URL}/builds", params=params)
        response.raise_for_status()
        builds = response.json()
        if not builds:
            print("No builds found.")
            return
        df = pd.DataFrame(builds)

        # Apply column filtering BEFORE renaming
        if include:
            # Only keep specified columns (use original column names)
            df = df[[col for col in include if col in df.columns]]
        if exclude:
            # Drop specified columns (use original column names)
            df = df.drop(
                columns=[col for col in exclude if col in df.columns],
                errors="ignore",
            )

        # Rename columns after filtering
        df = df.rename(
            columns={
                "id": "ID",
                "week": "Week",
                "rank": "Rank",
                "popularity": "PopRank",
                "pokemon": "Pokemon",
                "role": "Role",
                "pokemon_win_rate": "WR",
                "pokemon_pick_rate": "PR",
                "move_1": "M1",
                "move_2": "M2",
                "moveset_win_rate": "MWR",
                "moveset_pick_rate": "MPR",
                "moveset_true_pick_rate": "M@PR",
                "item": "Item",
                "moveset_item_win_rate": "M&I_WR",
                "moveset_item_pick_rate": "M&I_PR",
                "moveset_item_true_pick_rate": "M&I_@PR",
            }
        )
        text = df.to_string(index=False)
        try:
            print(colorize_role(text))
        except BrokenPipeError:
            # Handle pipe being closed (e.g., when piping to head)
            sys.stderr.close()
            pass
    except Exception as e:
        logger.error(f"Fetching builds failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Pokemon Unite Meta Analysis CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health", help="Check API health")

    get_builds_parser = subparsers.add_parser(
        "get-builds",
        help="Get builds with optional filters and column selection",
        description="Fetch and display Pokemon Unite builds with colorized output by role.",
        epilog="""Available columns for --include/--exclude:
  id, week, rank, popularity, pokemon, role, pokemon_win_rate, pokemon_pick_rate,
  move_1, move_2, moveset_win_rate, moveset_pick_rate, moveset_true_pick_rate,
  item, moveset_item_win_rate, moveset_item_pick_rate, moveset_item_true_pick_rate

Relevance strategies:
  any                  - Return all builds (no filtering)
  percentage           - Filter by moveset_item_true_pick_rate >= threshold (0.0-100.0)
  top_n                - Return top N builds by moveset_item_true_pick_rate
  cumulative_coverage  - Return builds until cumulative coverage >= threshold (0.0-100.0)
  quartile             - Return top quartile(s) (threshold: 1-4)

Example usage:
  %(prog)s --week Y2025m10d05 --include pokemon role moveset_item_win_rate
  %(prog)s --role Support --exclude id week rank
  %(prog)s --pokemon Pikachu --item "Attack Weight"
  %(prog)s --week Y2025m10d05 --relevance top_n --relevance-threshold 10
  %(prog)s --week Y2025m10d05 --sort-by moveset_item_win_rate --relevance percentage --relevance-threshold 5.0
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    get_builds_parser.add_argument(
        "--pokemon",
        type=str,
        help="Filter by Pokémon name (e.g., 'Pikachu', 'Charizard')",
    )
    get_builds_parser.add_argument(
        "--role",
        type=str,
        help="Filter by role (Support, Attacker, Speedster, Defender, All-Rounder)",
    )
    get_builds_parser.add_argument(
        "--week", type=str, help="Filter by week (format: Y2025m10d05)"
    )
    get_builds_parser.add_argument(
        "--item", type=str, help="Filter by held item name"
    )
    get_builds_parser.add_argument(
        "--relevance",
        type=str,
        choices=[
            "any",
            "percentage",
            "top_n",
            "cumulative_coverage",
            "quartile",
        ],
        help="Relevance strategy to apply (any, percentage, top_n, cumulative_coverage, quartile)",
    )
    get_builds_parser.add_argument(
        "--relevance-threshold",
        type=float,
        help="Threshold for relevance strategy (meaning varies by strategy)",
    )
    get_builds_parser.add_argument(
        "--sort-by",
        type=str,
        choices=[
            "pokemon",
            "role",
            "pokemon_win_rate",
            "pokemon_pick_rate",
            "moveset_win_rate",
            "moveset_pick_rate",
            "moveset_true_pick_rate",
            "item",
            "moveset_item_win_rate",
            "moveset_item_pick_rate",
            "moveset_item_true_pick_rate",
        ],
        help="Sort builds by specified field",
    )
    get_builds_parser.add_argument(
        "--include",
        nargs="*",
        type=str,
        metavar="COLUMN",
        help="Columns to include in output (space separated). Only these columns will be shown.",
    )
    get_builds_parser.add_argument(
        "--exclude",
        nargs="*",
        type=str,
        metavar="COLUMN",
        help="Columns to exclude from output (space separated). All columns except these will be shown.",
    )

    args = parser.parse_args()

    if args.command == "health":
        get_health()
    elif args.command == "get-builds":
        params = {}
        if args.pokemon:
            params["pokemon"] = args.pokemon
        if args.role:
            params["role"] = args.role
        if args.week:
            params["week"] = args.week
        if args.item:
            params["item"] = args.item
        if args.relevance:
            params["relevance"] = args.relevance
        if args.relevance_threshold is not None:
            params["relevance_threshold"] = args.relevance_threshold
        if args.sort_by:
            params["sort_by"] = args.sort_by
        get_builds(
            params if params else None,
            include=args.include,
            exclude=args.exclude,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
