"""
Metadata analysis module for Pokémon Unite builds.

This module retrieves and processes Pokémon build data from a database,
sorting and displaying it based on specific criteria such as moveset item true
pick rate and moveset item win rate. The output is color-coded for better
readability based on the role of each Pokémon.
"""

import re

import pandas as pd

from repository.build_repository import BuildRepository


def print_sorted_data():
    """
    Retrieves, processes, and prints sorted Pokémon build data from the latest
    table in the BuildRepository. The data is sorted by moveset item true pick
    rate and moveset item win rate, with columns renamed for readability.
    Builds are colorized based on their role (Support, Attacker, etc.) when
    printed.

    The function performs the following steps:
    - Retrieves the latest table from the BuildRepository.
    - Queries build data from the database and sorts it by
        'moveset_item_true_pick_rate'.
    - Selects the top 250 builds and sorts them by 'moveset_item_win_rate'.
    - Resets the index and drops unnecessary columns.
    - Renames columns for better readability.
    - Converts the sorted data to a string and applies colorization based on
      'role' using ANSI escape sequences.
    - Prints the resulting colored string.

    Note: The function assumes a specific database schema and column naming
    convention.
    """

    with BuildRepository() as build_repository:
        weeks = build_repository.get_available_weeks()
        week = weeks[0]

        # query builds of builds table for given week
        builds_query = pd.read_sql_query(
            f"SELECT * FROM builds WHERE week = '{week}'",
            build_repository.conn,
        )

    builds = builds_query.sort_values(
        "moveset_item_true_pick_rate", ascending=False
    )
    n_builds = 250
    builds = builds.head(n_builds)
    builds = builds.reset_index()
    builds.index = builds.index + 1

    threshold = builds.tail(1)["moveset_item_true_pick_rate"].iloc[0]
    # print(builds)
    print(f"Top {n_builds} builds from table {week}. Threshold: {threshold}")

    # builds = builds.sort_values("moveset_item_true_pick_rate", ascending=False)
    builds = builds.sort_values("moveset_item_win_rate", ascending=False)

    builds_sorted = builds.reset_index()
    builds_sorted.index = builds_sorted.index + 1
    # remove columns index and id
    builds_sorted = builds_sorted.drop(columns=["index", "id", "week"])

    # rename columns
    builds_sorted = builds_sorted.rename(
        columns={
            "level_0": "PopRank",
            "pokemon": "Pokemon",
            "role": "Role",
            "pkm_win_rate": "WR",
            "pkm_pick_rate": "PR",
            "move1": "M1",
            "move2": "M2",
            "moveset_win_rate": "MovesetWR",
            "moveset_pick_rate": "MovesetPR",
            "moveset_true_pick_rate": "Moveset@PR",
            "item": "Item",
            "moveset_item_win_rate": "M&I_WR",
            "moveset_item_pick_rate": "M&I_PR",
            "moveset_item_true_pick_rate": "M&I_@PR",
        }
    )

    # print all 1000 builds
    text = builds_sorted.to_string()
    # colorize the text lines with "Support" searching with regex
    text = re.sub(
        r"(.*Support.*)",
        r"\033[38;5;214m\1\033[0m",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"(.*Attacker.*)",
        r"\033[38;5;1m\1\033[0m",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"(.*Speedster.*)",
        r"\033[38;5;4m\1\033[0m",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(.*Defender.*)",
        r"\033[1;38;5;2m\1\033[0m",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(.*All-Rounder.*)",
        r"\033[38;5;93m\1\033[0m",
        text,
        flags=re.IGNORECASE,
    )
    print(text)


def main():
    """
    Main function
    """
    print_sorted_data()


if __name__ == "__main__":
    main()
