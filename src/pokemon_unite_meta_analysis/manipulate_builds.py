"""
ManipulateBuilds module for Pokémon Unite builds.

This module provides functionality to manipulate and analyze Pokémon build
data stored in a database. It includes classes and methods to sort, filter,
and retrieve builds based on various criteria.
"""

import json

from entity.build_response import BuildResponse
from entity.sort_by import SortBy
from pokemon_unite_meta_analysis.custom_log import LOG
from pokemon_unite_meta_analysis.relevance_strategy import RELEVANCE_STRATEGIES
from repository.build_repository import BuildRepository

# import rich


class ManipulateBuilds:
    """
    This is the constructor (`__init__`) of the `ManipulateBuilds` class. It
    initializes an instance of the class with two attributes:

    * `build_repository`: an instance of `BuildRepository`, which is assigned to
    the `self.build_repository` attribute.

    * `date`: a string representing a date, which is assigned to the `self.date`
    attribute.

    The constructor also logs an informational message ("Creating manipulate
    builds") using the `LOG` object.
    """

    def __init__(
        self,
        build_repository: BuildRepository,
        date: str,
    ):
        LOG.info("Creating manipulate builds")

        self.build_repository = build_repository
        self.date = date

    def _most_relevant(
        self,
        builds: list[BuildResponse],
        relevance: str,
        threshold: float,
        get_builds: callable,
    ) -> list[BuildResponse]:
        LOG.info("Getting n most relevant builds")
        LOG.debug("builds: %s", builds)
        LOG.debug("relevance: %s", relevance)
        LOG.debug("threshold: %s", threshold)

        if relevance not in RELEVANCE_STRATEGIES:
            raise ValueError(f"Invalid relevance: {relevance}")

        relevant_builds = RELEVANCE_STRATEGIES[relevance].apply(
            builds, threshold, get_builds=get_builds
        )
        return relevant_builds

    def _head(
        self, builds: list[BuildResponse], n: int = 0
    ) -> list[BuildResponse]:
        LOG.info("Getting head of builds")
        LOG.debug("builds: %s", builds)
        LOG.debug("n: %s", n)

        if n == 0:
            return builds

        return builds[:n]

    def _sort(
        self, builds: list[BuildResponse], sort_by: SortBy
    ) -> list[BuildResponse]:
        LOG.info("Sorting builds")
        LOG.debug("builds: %s", builds)
        LOG.debug("sort_by: %s", sort_by)

        data = sorted(
            builds,
            key=lambda build: getattr(build, sort_by.value),
            reverse=True,
        )

        return data

    def _get_builds(self) -> list[BuildResponse]:
        LOG.info("Getting builds from table")

        return self.build_repository.get_all_builds_by_table(self.date)

    def _return_builds_as_json(self, builds: list[BuildResponse]) -> list[dict]:
        LOG.info("Returning builds as json")
        LOG.debug("builds: %s", builds)

        list_builds = [
            {
                "rank": idx + 1,
                "pokemon": build.pokemon,
                "role": build.role,
                "pokemon_win_rate": build.pokemon_win_rate,
                "pokemon_pick_rate": build.pokemon_pick_rate,
                "move_1": build.move_1,
                "move_2": build.move_2,
                "moveset_win_rate": build.moveset_win_rate,
                "moveset_pick_rate": build.moveset_pick_rate,
                "moveset_true_pick_rate": build.moveset_true_pick_rate,
                "item": build.item,
                "moveset_item_win_rate": build.moveset_item_win_rate,
                "moveset_item_pick_rate": build.moveset_item_pick_rate,
                "moveset_item_true_pick_rate": build.moveset_item_true_pick_rate,
            }
            for idx, build in enumerate(builds)
        ]

        dict_builds = {"builds": list_builds}
        json_builds = json.dumps(dict_builds)

        return json_builds

    def run(
        self,
        sort_by: SortBy,
        top_n: int = 0,
        relevance: str = "any",
        relevance_threshold: float = 0.0,
        print_result: bool = False,
    ) -> list[dict]:
        """
        Run manipulate builds

        Args:
            sort_by (SortBy): Sort by
            top_n (int, optional): Top n. Defaults to 0.
            relevance (str, optional): Relevance. Defaults to "any".
            relevance_threshold (float, optional): Relevance threshold. Defaults
                to 0.0.
            print_result (bool, optional): Print result. Defaults to False.

        Returns:
            list[dict]: List of builds
        """
        LOG.info("Running manipulate builds")
        LOG.debug("sort_by: %s", sort_by)
        LOG.debug("top_n: %s", top_n)
        LOG.debug("relevance: %s", relevance)
        LOG.debug("relevance_threshold: %s", relevance_threshold)
        LOG.debug("print_result: %s", print_result)

        builds = self._get_builds()

        relevant_builds = self._most_relevant(
            builds, relevance, relevance_threshold, get_builds=lambda: builds
        )

        sorted_builds = self._sort(relevant_builds, sort_by)
        sorted_builds = self._head(sorted_builds, top_n)

        result = self._return_builds_as_json(sorted_builds)

        # if print_result:
        #     rich.print_json(result)

        return result


def main():
    """
    Main function
    """
    LOG.info("Running manipulate builds")

    date = "Y2025m08d03"
    build_repository = BuildRepository()
    manipulate_builds = ManipulateBuilds(build_repository, date)
    manipulate_builds.run(
        SortBy.MOVESET_ITEM_WIN_RATE,
        50,
        "moveset_item_true_pr",
        2,
        True,
    )


if __name__ == "__main__":
    LOG.info("Running as main")

    main()
