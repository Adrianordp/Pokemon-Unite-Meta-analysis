"""
Defines relevance strategies for filtering builds based on different criteria.
"""

from typing import Callable, Protocol

from entity.build_response import BuildResponse
from pokemon_unite_meta_analysis.relevance import Relevance


class RelevanceStrategy(Protocol):
    def __call__(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]: ...


def relevance_any(
    builds: list[BuildResponse],
    threshold: float,
    get_builds: Callable[[], list[BuildResponse]],
) -> list[BuildResponse]:
    return builds


def relevance_moveset_item_true_pr(
    builds: list[BuildResponse],
    threshold: float,
    get_builds: Callable[[], list[BuildResponse]],
) -> list[BuildResponse]:
    return [
        build
        for build in builds
        if build.moveset_item_true_pick_rate >= threshold
    ]


def relevance_position_of_popularity(
    builds: list[BuildResponse],
    threshold: float,
    get_builds: Callable[[], list[BuildResponse]],
) -> list[BuildResponse]:
    position = int(threshold - 1)
    sorted_builds = sorted(
        get_builds(),
        key=lambda build: build.moveset_item_true_pick_rate,
        reverse=True,
    )
    cut_value = sorted_builds[position].moveset_item_true_pick_rate
    return [
        build
        for build in builds
        if build.moveset_item_true_pick_rate >= cut_value
    ]


RELEVANCE_STRATEGIES: dict[Relevance, RelevanceStrategy] = {
    Relevance.ANY: relevance_any,
    Relevance.MOVESET_ITEM_TRUE_PR: relevance_moveset_item_true_pr,
    Relevance.POSITION_OF_POPULARITY: relevance_position_of_popularity,
    # Add new strategies here as needed
}
