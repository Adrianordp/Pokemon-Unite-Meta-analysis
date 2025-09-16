"""
ManipulateBuilds module
"""

import json
from enum import Enum

from entity.build import Build
from repository.build_repository import BuildRepository
from util.log import setup_custom_logger

# import rich


LOG = setup_custom_logger("manipulate_builds")


class SortBy(Enum):
    """
    SortBy enum class
    """

    POKEMON = "pokemon"
    ROLE = "role"
    POKEMON_WIN_RATE = "pokemon_win_rate"
    POKEMON_PICK_RATE = "pokemon_pick_rate"
    MOVE_1 = "move_1"
    MOVE_2 = "move_2"
    MOVESET_WIN_RATE = "moveset_win_rate"
    MOVESET_PICK_RATE = "moveset_pick_rate"
    MOVESET_TRUE_PICK_RATE = "moveset_true_pick_rate"
    ITEM = "item"
    MOVESET_ITEM_WIN_RATE = "moveset_item_win_rate"
    MOVESET_ITEM_PICK_RATE = "moveset_item_pick_rate"
    MOVESET_ITEM_TRUE_PICK_RATE = "moveset_item_true_pick_rate"


class Relevance(Enum):
    """
    Relevance enum class
    """

    ANY = "any"
    MOVESET_ITEM_TRUE_PR = "moveset_item_true_pr"
    POSITION_OF_POPULARITY = "position_of_popularity"


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
        self, builds: list[Build], relevance: Relevance, threshold: float
    ) -> list[Build]:
        LOG.info("Getting n most relevant builds")
        LOG.debug("builds: %s", builds)
        LOG.debug("relevance: %s", relevance)
        LOG.debug("threshold: %s", threshold)

        if relevance == Relevance.ANY:
            pass
        elif relevance == Relevance.MOVESET_ITEM_TRUE_PR:
            builds = [
                build
                for build in builds
                if build.moveset_item_true_pick_rate >= threshold
            ]
        elif relevance == Relevance.POSITION_OF_POPULARITY:
            position = int(threshold - 1)
            builds = sorted(
                self._get_builds(),
                key=lambda build: build.moveset_item_true_pick_rate,
                reverse=True,
            )
            cut_value = builds[position].moveset_item_true_pick_rate
            builds = [
                build
                for build in builds
                if build.moveset_item_true_pick_rate >= cut_value
            ]
        else:
            raise ValueError(f"Relevance {relevance} is not supported")

        return builds

    def _head(self, builds: list[Build], n: int = 0) -> list[Build]:
        LOG.info("Getting head of builds")
        LOG.debug("builds: %s", builds)
        LOG.debug("n: %s", n)

        if n == 0:
            return builds

        return builds[:n]

    def _sort(self, builds: list[Build], sort_by: SortBy) -> list[Build]:
        LOG.info("Sorting builds")
        LOG.debug("builds: %s", builds)
        LOG.debug("sort_by: %s", sort_by)

        data = sorted(
            builds,
            key=lambda build: getattr(build, sort_by.value),
            reverse=True,
        )

        return data

    def _get_builds(self) -> list[Build]:
        LOG.info("Getting builds from table")

        return self.build_repository.get_all_builds_by_table(self.date)

    def _return_builds_as_json(self, builds: list[Build]) -> list[dict]:
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
        relevance: Relevance = Relevance.ANY,
        relevance_threshold: float = 0.0,
        print_result: bool = False,
    ) -> list[dict]:
        """
        Run manipulate builds

        Args:
            sort_by (SortBy): Sort by
            top_n (int, optional): Top n. Defaults to 0.
            relevance (Relevance, optional): Relevance. Defaults to
                Relevance.ANY.
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
            builds, relevance, relevance_threshold
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
        Relevance.MOVESET_ITEM_TRUE_PR,
        2,
        True,
    )


if __name__ == "__main__":
    LOG.info("Running as main")

    main()
